# -*- coding: utf-8 -*-
from django.core.files.storage import Storage, FileSystemStorage


class CustomFileSystemStorage(FileSystemStorage):
    def _save(self, name, content):
        return super(CustomFileSystemStorage, self)._save(name, content)


class CloudStorage(Storage):
    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        pass