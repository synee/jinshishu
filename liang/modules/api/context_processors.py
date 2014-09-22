# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from liang.base.kits import jsonify


def contents(request):
    """
    Content Types
    :param request:
    :return:
    """
    contents = ContentType.objects.all()
    contents_json = dict()
    for content in contents:
        # key = "%s.%s" % (content.app_label, content.model)
        key = content.model
        contents_json[key] = content.id
    return {
        'CONTENTS': contents,
        'CONTENTS_JSON': jsonify(contents_json)
    }