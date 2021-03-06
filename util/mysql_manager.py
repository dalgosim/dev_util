# -*- coding: utf-8 -*-

import sys
import pandas as pd
import pymysql
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
import logging

from dev_util.util import logger, config


class MysqlController:

    def __init__(self, host=None, user=None, password=None, db=None, logging_level=logging.INFO):
        self.logger = logger.APP_LOGGER
        self.logger.setLevel(logging_level)

        db_config = config.CONFIG.MYSQL_CONFIG
        host = host if host is not None else db_config.MYSQL_HOST
        user = user if user is not None else db_config.MYSQL_USER
        password = password if password is not None else db_config.MYSQL_PASSWD
        db = db if db is not None else db_config.MYSQL_DB
        
        # MySQL Connection 연결
        db_config = config.CONFIG.MYSQL_CONFIG
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    password=password,
                                    db=db,
                                    charset='utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        self.engine = create_engine(
                        '''mysql+pymysql://{user}:{passwd}@{svr}/{db_name}?charset={charset}'''.format(
                            user=user,
                            passwd=password,
                            svr=host,
                            db_name=db,
                            charset='utf8'),
                            encoding='utf8')
    def __del__(self):
        if self.conn is not None:
            self.conn.close()
        if self.curs is not None:
            self.curs.close()

    def select(self, query):
        # ==== select example ====
        self.curs.execute(query)

        # 데이타 Fetch
        rows = self.curs.fetchall()
        return rows

    def insert(self, query):
        # ==== insert example ====
        # sql = """insert into customer(name,category,region)
        #         values (%s, %s, %s)"""
        # self.curs.execute(sql, ('이연수', 2, '서울'))
        self.curs.execute(query)
        self.conn.commit()

    def update(self, query):
        self.curs.execute(query)
        self.conn.commit()

    def delete(self, query):
        self.update(query)

    def select_dataframe(self, query, log=''):
        self.logger.debug(f'Select Datarame : {query}')
        df = pd.read_sql(query, self.engine)
        self.logger.debug(f'Select complete')
        return df

    def insert_dataframe(self, df, table, index=False, ignore_duplicate=True):
        try:
            self.logger.debug(f'Insert Datarame into {table} : {len(df)}')
            df.to_sql(name=table, con=self.engine, index=index, if_exists='append')
            self.logger.debug(f'Insert complete')
        except Exception as e:
            # 여러줄 오류시 한줄씩 넣기
            for i in range(len(df)):
                row = df.iloc[[i]]
                try:
                    row.to_sql(name=table, con=self.engine, index=index, if_exists='append')
                except IntegrityError as e:
                    if not ignore_duplicate:
                        self.logger.debug(f'Duplicated Row ({table}) : {e.args[0]}')
                except Exception as e:
                    self.logger.error(f'Insert Datarame Error ({table}) : {e}')
