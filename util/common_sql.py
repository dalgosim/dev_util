# -*- coding: utf-8 -*-
from dev_util.util import config, mysql_manager


def get_company_list(limit=0):
    _mysql = mysql_manager.MysqlController()
    table = config.CONFIG.MYSQL_CONFIG.TABLES.COMPANY_LIST_TABLE
    limit_q = f'''LIMIT {limit}''' if limit > 0 else ''
    query = f'''SELECT distinct cmp_cd FROM {table} {limit_q};'''
    return _mysql.select_dataframe(query, log='get_company_list')

def get_recent_price(cmp_cd, days=121, order='DESC'):
    _mysql = mysql_manager.MysqlController()
    table = config.CONFIG.MYSQL_CONFIG.TABLES.PRICE_TABLE
    query = f'''
    SELECT distinct *
    FROM {table}
    WHERE LEFT(cmp_cd,6)="{cmp_cd}"
    ORDER BY date {order}
    LIMIT {days};
    '''
    return _mysql.select_dataframe(query, log='get_price_list')
