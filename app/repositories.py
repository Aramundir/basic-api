# -*- coding: utf-8 -*-

from sqlalchemy import exc, desc

from app.infrastructure.database import orm


class AbstractModel(object):
    query = None
    _order_by = None


    class NotExist(Exception):
        pass


    class RepositoryError(Exception):
        pass

    @classmethod
    def create_from_json(cls, json_data, commit=False):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db(commit)
            return instance
        except exc.IntegrityError as ex:
            cls.rollback_db()
            raise cls.RepositoryError(ex)

    @classmethod
    def order_by(cls):
        order_by = [desc(cls.id)]
        if cls._order_by:
            order_by = cls._order_by
        return order_by

    @classmethod
    def list_with_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).order_by(*cls.order_by()).all()

    @classmethod
    def list_with_filter_and_paginate(cls, page, page_size, **kwargs):
        paginate = cls.query.filter_by(**kwargs).order_by(*cls.order_by()).paginate(page=page, per_page=page_size, error_out=False)
        return paginate.items, paginate.total

    @classmethod
    def list_all(cls):
        return cls.query.order_by(*cls.order_by()).all()

    @classmethod
    def delete_all(cls):
        return cls.list_all().delete()

    @classmethod
    def get_with_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).one_or_none()

    @classmethod
    def get(cls, item_id):
        item = cls.query.get(item_id)
        if not item:
            raise cls.NotExist
        else:
            return item

    @classmethod
    def rollback_db(cls):
        orm.session.rollback()

    def save_db(self, commit=True):
        orm.session.add(self)
        orm.session.flush()
        if commit:
            orm.session.commit()
        orm.session.refresh(self)

    def delete_db(self):
        try:
            orm.session.delete(self)
            orm.session.flush()
        except exc.IntegrityError as ex:
            raise self.RepositoryError(ex)

    def update_from_json(self, json_data):
        try:
            self.set_values(json_data)
            self.save_db()
            return self
        except exc.IntegrityError as ex:
            raise self.RepositoryError(ex)

    def set_values(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, json_data.get(key, getattr(self, key)))
