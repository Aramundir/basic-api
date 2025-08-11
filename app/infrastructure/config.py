#  -*- coding: utf-8 -*-
"""
Config File for enviroment variables
"""
from __future__ import unicode_literals

import os
from importlib import import_module

from app.infrastructure import exceptions


class Config(object):
    """
    Base class for all config variables
    """
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    AMBIENTE = 'production'

    def __init__(self):
        if self.AMBIENTE is None:
            raise TypeError('You should use one of the specialized config class')

        self.API_TOKEN = os.environ['API_TOKEN']
        self.SECRET_KEY = os.environ['SECRET_KEY']

        self.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    """
    Production Config... this is the real thing
    """
    AMBIENTE = 'production'


class StagingConfig(Config):
    """
    Staging Config is for... staging things
    """
    AMBIENTE = 'staging'


class DevelopmentConfig(Config):
    """
    Development Config... this is your home developer!
    """
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(DevelopmentConfig):
    """
    Test Config... You should be testing right now instead reading docs!!!
    """
    TESTING = True
    AMBIENTE = 'test'


def get_config():
    """
    Get the Config Class instance defined in APP_SETTINGS environment variable
    :return The config class instance
    :rtype: Config
    """
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, None)
    if not config_class:
        raise exceptions.ConfigClassNotFound('Unable to find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class()
