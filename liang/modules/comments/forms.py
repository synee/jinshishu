# -*- coding: utf-8 -*-
from django.contrib.comments import CommentForm
from app.forms.angular_model import NgModelFormMixin
from .models import CustomComment


class CustomCommentForm(CommentForm):
    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return CustomComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
        data = super(CustomCommentForm, self).get_comment_create_data()
        data['title'] = self.cleaned_data['title']
        return data