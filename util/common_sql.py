# -*- coding: utf-8 -*-
from dev_util.util import config, mysql_manager


def get_company_list(limit=0):
    _mysql = mysql_manager.MysqlController()
    table = config.CONFIG.MYSQL_CONFIG.TABLES.COMPANY_LIST_TABLE
    limit_q = f'''LIMIT {limit}''' if limit > 0 else ''
    query = f'''SELECT distinct cmp_cd FROM {table} {limit_q};'''
    return _mysql.select_dataframe(query, log='get_company_list')

def get_recent_price(cmp_cd, last_date, days=121, order='DESC'):
    _mysql = mysql_manager.MysqlController()
    table = config.CONFIG.MYSQL_CONFIG.TABLES.PRICE_TABLE
    query = f'''
    SELECT *
    FROM {table}
    WHERE cmp_cd="{cmp_cd}"
        AND date<="{last_date}"
    ORDER BY date {order}
    LIMIT {days};
    '''
    return _mysql.select_dataframe(query, log='get_price_list')

def get_company_list_without_del():
    _mysql = mysql_manager.MysqlController()
    cmp_table = config.CONFIG.MYSQL_CONFIG.TABLES.COMPANY_LIST_TABLE
    del_table = config.CONFIG.MYSQL_CONFIG.TABLES.COMPANY_DEL_LIST_TABLE
    query = f'''
    SELECT c.cmp_cd
    FROM {cmp_table} c
    LEFT JOIN {del_table} cd
    ON c.cmp_cd=cd.cmp_cd
    WHERE cd.cmp_cd IS NULL;
    '''
    return _mysql.select_dataframe(query, log='get_company_list_without_del')
