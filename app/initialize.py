# -*- coding: utf-8 -*-

from flask import Flask

from app import api, config
from app.infrastructure import database

web_app = Flask(__name__)
web_app.config.from_object(config)

database.register_orm(web_app)
migrate = database.register_migration(web_app)
api.create_api(web_app)
