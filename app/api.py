# -*- coding: utf-8 -*-

from flask_restful import Api


def create_api(app):
    from app import resources
    api = Api(app)