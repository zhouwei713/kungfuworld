'''
Created on 2017415

@author: zhouandy

Update on 20180220
'''
import os
# from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[KungFuWorld]'
    FLASKY_MAIL_SENDER = 'kungfurealm@gmail.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 5
    UPLOAD_FOLDER = os.getcwd() + '\\app\\static\\avatar\\'
    FLASKY_FOLLOWERS_PER_PAGE = 5
    FLASKY_COMMENTS_PER_PAGE = 5
    MAX_SEARCH_RESULTS = 50
    ONLINE_LAST_MINUTES = 5
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLALCHEMY_DATABASE_URI = 'postgres://xqsibfufbyusjl:43d0a56c954439675f98a97dc354ced805a18e73548a7e8c71791a2b32f35d27@ec2-54-235-72-121.compute-1.amazonaws.com:5432/d5lp58cqt398vd'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/zhouluobo'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLURI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'kungfu.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
