# -*- coding=utf-8 -*-

'''
要注意的是， 这里可以写入多个配置， 就仿照DevelopmentConfig这个类一样，
继承Config类即可。
并在最下方的Config字典里添加对应的key：value。
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkey_erqerq'  #填入密钥
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <wren@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        import logging
        from logging.handlers import RotatingFileHandler
        _handler = RotatingFileHandler(\
                'app.log', maxBytes=10000, backupCount=1)
        _handler.setLevel(logging.WARNING)
        app.logger.addHandler(_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask_def'
    #SQLALCHEMY链接数据库都是以URI方式格式为 'mysql://账户名:密码@地址/数据库表名'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }
