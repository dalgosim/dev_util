# -*- coding: utf-8 -*-
import json
from dotmap import DotMap

from dev_util.util import timer, logger

_logger = logger.APP_LOGGER
CONFIG = DotMap()
BASIS_DATE = timer.get_now('%Y-%m-%d')
TEST_MODE = True

def load_config(config_name='REAL_DB', path='config.json'):
    global CONFIG, TEST_MODE, BASIS_DATE

    AUTH_PATH = './auth/mysql_auth.json'

    # set date
    if timer.get_now_hour() < 16: #4시 이전에는 전날 기준으로 가져오기
        BASIS_DATE = timer.get_yesterday('%Y-%m-%d')

    # load scheduler config
    try:
        with open(path) as f:
            config_data = json.load(f)
    except:
        config_data = {}
        _logger.debug('There is no config')
    
    # load database config
    try:
        with open(AUTH_PATH) as f:
            auth_data = json.load(f)
            auth_data['MYSQL_CONFIG'] = auth_data['MYSQL_SVR'][config_name]
            auth_data.pop('MYSQL_SVR')
            _logger.debug(f'Loaded database config')
    except:
        auth_data = {}
        _logger.debug('There is no auth config')

    # merge config
    merged_dict = {**config_data, **auth_data}
    CONFIG = DotMap(merged_dict)
