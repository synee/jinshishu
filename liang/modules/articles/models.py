# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2


class Book(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=u'书籍名称')
    owner = models.ForeignKey(to='accounts.User', related_name='books')
    cover = models.ImageField(verbose_name=u"封面", upload_to="cover", null=True, default='cover/default_book.png')
    date_created = models.DateTimeField(default=lambda *args: timezone.now())
    date_updated = models.DateTimeField(default=lambda *args: timezone.now())

    @property
    def published_articles(self):
        return self.articles.filter(status=DRAFT)

    def get_absolute_url(self):
        return "/p/book/%s" % (self.pk, )

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = ((DRAFT, _(u'草稿')),
                      (HIDDEN, _(u'隐藏')),
                      (PUBLISHED, _(u'发表')))
    # 标题
    title = models.CharField(max_length=64, verbose_name=u'标题')
    book = models.ForeignKey(to="Book", null=True, related_name='articles')
    author = models.ForeignKey(to='accounts.User', related_name='articles')
    content = models.TextField(blank=True, verbose_name=_(u'正文'))
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
        """
        Checks if an entry is visible and published.
        """
        return self.is_actual and self.status == PUBLISHED

    def get_absolute_url(self):
        return "/p/%s" % (self.pk, )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('book', 'title'),)
