# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from django.conf import settings
from django.contrib.humanize.templatetags import humanize
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from liang.base.decorator import time_spend
from liang.base.models import BaseModel

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2


class AbstractBook(BaseModel):
    name = models.CharField(max_length=64, verbose_name=u'书籍名称')
    rate = models.FloatField(default=5, verbose_name=u'评分')
    rate_users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='rate_books')
    author_name = models.CharField(max_length=64, blank=True, verbose_name=u'作者名称')
    cover = models.ImageField(verbose_name=u"封面", upload_to="cover", null=True, default='cover/default_book.png')
    summary = models.CharField(max_length=300, blank=True, verbose_name="概要")
    date_created = models.DateTimeField(default=lambda *args: timezone.now())
    date_updated = models.DateTimeField(default=lambda *args: timezone.now())

    @property
    def published_articles(self):
        return self.articles.filter(status=PUBLISHED)

    def get_absolute_url(self):
        return "/p/book/%s" % (self.pk, )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Book(AbstractBook):
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='books')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_updated = timezone.now()
        saved = super(Book, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)
        return saved

    @classmethod
    def search(cls, q=None, order_by='-pk', *args, **kwargs):
        if not q:
            q = ''
        return cls.objects.filter(name__contains=q).order_by(order_by)

    def to_dict(self):
        json_dict = self.__dict__
        json_dict.update({
            "owner": self.owner,
            "author_name": self.author_name if not not self.author_name else str(self.owner),
            "date_created": humanize.naturaltime(self.date_created),
            "date_updated": humanize.naturaltime(self.date_updated)
        })
        return json_dict

    def delete(self, using=None):
        self.articles.update(enable=False)
        self.enable = False
        return super(Book, self).delete(using=using)

    class Meta:
        abstract = False


class Article(BaseModel):
    STATUS_CHOICES = ((DRAFT, _(u'草稿')),
                      (HIDDEN, _(u'隐藏')),
                      (PUBLISHED, _(u'发表')))
    # 标题
    title = models.CharField(max_length=64, verbose_name=u'标题')
    book = models.ForeignKey(to="Book", null=True, related_name='articles')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='articles')
    author_name = models.CharField(max_length=64, blank=True, verbose_name=u'作者名称')
    summary = models.TextField(blank=True, max_length=140, verbose_name=_(u'简述'))
    content = models.TextField(blank=True, max_length=100000, verbose_name=_(u'正文'))
    slug = models.SlugField(
        _('slug'), max_length=255,
        unique_for_date='date_created',
        help_text=_("Used to build the entry's URL."))
    status = models.IntegerField(
        _('状态'), db_index=True,
        choices=STATUS_CHOICES, default=DRAFT)
    start_publication = models.DateTimeField(
        _('start publication'),
        db_index=True, blank=True, null=True,
        help_text=_('Start date of publication.'))
    end_publication = models.DateTimeField(
        _('end publication'),
        db_index=True, blank=True, null=True,
        help_text=_('End date of publication.'))
    date_created = models.DateTimeField(default=lambda *args: timezone.now())
    date_updated = models.DateTimeField(default=lambda *args: timezone.now())

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_updated = timezone.now()
        self.summary = (''.join(BeautifulSoup(self.content).findAll(text=True)))[0: 140] + "..."
        saved = super(Article, self).save(force_insert=force_insert,
                                          force_update=force_update,
                                          using=using,
                                          update_fields=update_fields)
        self.book.date_updated = timezone.now()
        self.book.save()
        return saved

    @classmethod
    def new_instance(cls, book, user, title=None, title_index=0):
        if not title:
            title = u'新建文章'
        if title_index > 0:
            query_title = "%s %d" % (title, title_index)
        else:
            query_title = title
        exist_book = cls.objects.filter(book=book, author=user, title=query_title)
        if len(exist_book) > 0:
            title_index += 1
            return cls.new_instance(book=book,
                                    user=user,
                                    title=title,
                                    title_index=title_index)
        else:
            article = cls(book=book, author=user, title=query_title)
            article.save()
            return article

    @property
    def is_actual(self):
        """
        Checks if an entry is within his publication period.
        """
        now = timezone.now()
        if self.start_publication and now < self.start_publication:
            return False

        if self.end_publication and now >= self.end_publication:
            return False
        return True

    @property
    def is_visible(self):
        return self.is_actual and self.status == PUBLISHED

    def get_absolute_url(self):
        return "/p/%s" % (self.pk, )

    @classmethod
    @time_spend
    def search(cls, q=None, order_by='-pk', *args, **kwargs):
        if not q:
            q = ''
        return cls.objects.filter(title__contains=q).order_by(order_by)

    @time_spend
    def to_dict(self):
        json_dict = self.__dict__
        json_dict.update({
            "book": self.book,
            "author": self.author,
            "author_name": self.author_name if not not self.author_name else str(self.author),
            "date_created": humanize.naturaltime(self.date_created),
            "date_updated": humanize.naturaltime(self.date_updated)
        })
        if json_dict.has_key('content'):
            json_dict.pop('content')
        return json_dict

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('book', 'title'),)
        ordering = ("-date_updated", )




