# -*- coding: utf-8 -*-
from django import forms
from app.forms.angular_model import NgModelFormMixin
from liang.modules.articles.models import Book, Article


class BookForm(NgModelFormMixin, forms.ModelForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['cover'].required = False
        self.fields['owner'].widget = forms.HiddenInput()
        self.fields['owner'].initial = request.user

    class Meta:
        model = Book
        fields = ['cover', 'name', 'owner']


class ArticleForm(NgModelFormMixin, forms.ModelForm):

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget = forms.HiddenInput()
        self.fields['author'].initial = request.user
        self.fields['book'].queryset = Book.objects.filter(owner=request.user.id)
        if self.instance and self.instance.book:
            self.request.book = self.instance.book

        if hasattr(self.request, "book"):
            self.fields['book'].widget = forms.HiddenInput()
            self.fields['book'].initial = self.request.book

    class Meta:
        model = Article
        fields = ['book', 'title', 'content', 'author']



