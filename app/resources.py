# -*- coding: utf-8 -*-
import json
import re

from flask import request
from flask_restful import Resource


class ResourceBase(Resource):

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name):
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    @property
    def payload(self):
        payload = {}
        try:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        except Exception:
            pass
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    def return_ok(self):
        return {"result": "OK"}, 200

    def return_delete_ok(self):
        return {}, 204

    def return_not_authorized(self):
        return {"result": "Not Authorized"}, 401

    def return_not_found(self):
        return {"result": "Not Found"}, 404

    def return_not_allowed(self):
        return {"result": "Method Not Allowed"}, 405

    def return_bad_request(self, message):
        return {"result": "Bad Request", "message": message}, 400

    def response(self, data_dict, code=200):
        return self.transform_key(data_dict, self.snake_to_camel), code

    def response_with_error(self, data_dict, status_code=500, extra=None):
        if extra is None:
            extra = {}
        try:
            data_dict['message'] = json.loads(data_dict['message'])
        except:
            pass
        return self.response(data_dict, status_code)


class HealthcheckResource(Resource):
    def get(self):
        return {"result": "OK"}, 200