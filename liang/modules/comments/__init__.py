# -*- coding: utf-8 -*-
from .forms import CustomCommentForm
from .models import CustomComment


def get_model():
    return CustomComment


def get_form():
    return CustomCommentForm