# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from liang.modules.accounts.models import User


class PeopleDetail(DetailView):
    model = User