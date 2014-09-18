from django.shortcuts import render
from django.views.generic import TemplateView
from liang.modules.articles.models import Book


def home(request, *args, **kwargs):
    book_new = Book.objects.filter().order_by('-id').all()[0:10]

    return render(request, 'search.html', {
        'book_new': book_new
    })
    # return render(request, 'index.html', {
    #     'book_new': book_new
    # })


class ExploreView(TemplateView):
    template_name = "dashboard.html"
