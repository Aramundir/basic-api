# -*- coding: utf-8 -*-

from app.infrastructure import exceptions


class Entity(object):
    repository = None

    @classmethod
    def list_all(cls):
        return [cls.create_with_instance(instance) for instance in cls.repository.list_all()]

    @classmethod
    def list_with_filter(cls, **filter_params):
        return [cls.create_with_instance(instance) for instance in cls.repository.list_with_filter(**filter_params)]

    @classmethod
    def list_with_filter_and_paginate(cls, page, page_size, **filter_params):
        pages = cls.repository.list_with_filter_and_paginate(page, page_size, **filter_params)
        return [cls.create_with_instance(instance) for instance in pages[0]], pages[1]

    @classmethod
    def create_new(cls, json_data, commit=False):
        try:
            return cls(cls.repository.create_from_json(json_data, commit))
        except cls.repository.RepositoryError as ex:
            if 'duplicate key value violates unique' in str(ex):
                raise exceptions.AlreadyExist('Entity with {} already exists in repository'.format(json_data))

    @classmethod
    def create_with_id(cls, entity_id):
        instance = cls.repository.get(entity_id)
        return cls.create_with_instance(instance)

    @classmethod
    def create_with_instance(cls, instance):
        if instance is None:
            raise exceptions.NotExist('Tryed to create entity with instance None. Check the stack trace to see the origin')
        return cls(instance)

    def __init__(self, instance=None):
        self.instance = instance
        self.id = None
        if instance is not None:
            self.id = instance.id

    def save(self):
        self.instance.save_db()