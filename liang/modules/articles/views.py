# -*- coding: utf-8 -*-
import json
import bleach
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from liang.base.views import ApiView
from liang.modules.articles.forms import ArticleForm, BookForm
from liang.modules.articles.models import Article, Book


class BookView(DetailView):
    model = Book


class BookCreate(CreateView):
    model = Book
    form_class = BookForm

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({
            "request": self.request,
        })
        return form_class(**kwargs)


class BookList(ListView):
    model = Book


class ArticleView(DetailView):
    model = Article


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Article

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({
            "request": self.request
        })
        return form_class(**kwargs)

    def get(self, request, book_id=None, *args, **kwargs):
        if book_id:
            book = Book.objects.get(pk=book_id)
            request.book = book
        return super(ArticleCreate, self).get(request, *args, **kwargs)

    @property
    def success_url(self, *args, **kwargs):
        return "/p/%s" % self.object.pk


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({
            "request": self.request
        })
        return form_class(**kwargs)


class WriterApiView(ApiView):

    def action_article(self, request, *args, **kwargs):
        pk = request.GET.get('pk')
        article = Article.objects.get(pk=pk)
        return article.__dict__

    def action_article_get(self, request, *args, **kwargs):
        data = request.GET
        book_id = data.get('book')
        return Book.objects.get(pk=book_id).articles.all()

    def action_article_search(self, request, page_index, page_size, *args, **kwargs):
        q = request.GET.get('q')
        if not q: q = ''
        return Article.objects.filter(title__contains=q).all()[page_index: page_size]

    def action_article_create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        article = Article.new_instance(book=Book.objects.get(pk=data.pop('book')), user=request.user)
        return Article.objects.get(pk=article.pk)

    def action_article_update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        pk = data.get('id')
        article = get_object_or_404(Article, pk=pk)
        data.update({
            'author': request.user.id,
            'book': article.book_id,
        })
        form = ArticleForm(request=request, data=data, instance=article)
        if form.is_valid():
            article = form.save()
            return article
        return {
            'errors': form.errors,
        }

    def action_article_delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        article_id = data.get('id')
        article = Article.objects.get(pk=article_id)
        article.delete()
        return {
            "success": Article.objects.filter(pk=article_id).count() == 0
        }

    def action_book_get(self, request, *args, **kwargs):
        return request.user.books.all()

    def action_book_search(self, request, page_index, page_size, *args, **kwargs):
        q = request.GET.get('q')
        return Book.search(q=q)[page_index: page_size]

    def action_book_create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        data.update({
            'owner': request.user.id
        })
        form = BookForm(request=request, data=data)
        if form.is_valid():
            book = form.save()
            return book
        return {
            "errors": form.errors
        }

    def action_book_update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        pk = data.get('id')
        book = get_object_or_404(Book, pk=pk)
        data.update({
            'owner': request.user.id
        })
        form = BookForm(request=request, data=data, instance=book)
        if form.is_valid():
            book = form.save()
            return book
        return {
            "success": False
        }

    def action_book_delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        book_id = data.get('id')
        book = Book.objects.get(pk=book_id)
        book.delete()
        return {
            "success": not book.enable
        }


