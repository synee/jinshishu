from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
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

