# -*- coding: utf-8 -*-


class Dataset(object):
    request = None
    args = []
    kwargs = {}
    model = None
    instance = None


class DatasetMixin(object):
    @classmethod
    def get_dataset(cls):
        return cls._dataset