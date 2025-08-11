# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

orm = None


def register_orm(web_app):
    global orm
    orm = SQLAlchemy(web_app)


def register_migration(web_app):
    from app import repositories
    return Migrate(web_app, orm)
