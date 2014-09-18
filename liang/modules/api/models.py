# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.html import linebreaks, strip_tags

from django.utils.translation import ugettext_lazy as _
from liang.modules.api.markups import markdown, textile, restructuredtext
from liang.modules.api.preview import HTMLPreview
from liang.modules.tagging.models import Tag

MARKUP_LANGUAGE = getattr(settings, 'ZINNIA_MARKUP_LANGUAGE', 'html')


class ContentEntry(models.Model):
    """
    Abstract content model class providing field
    and methods to write content inside an entry.
    """
    content = models.TextField(_('content'), blank=True)

    @property
    def html_content(self):
        """
        Returns the "content" field formatted in HTML.
        """
        if '</p>' in self.content:
            return self.content
        elif MARKUP_LANGUAGE == 'markdown':
            return markdown(self.content)
        elif MARKUP_LANGUAGE == 'textile':
            return textile(self.content)
        elif MARKUP_LANGUAGE == 'restructuredtext':
            return restructuredtext(self.content)
        return linebreaks(self.content)

    @property
    def html_preview(self):
        """
        Returns a preview of the "content" field formmated in HTML.
        """
        return HTMLPreview(self.html_content)

    @property
    def word_count(self):
        """
        Counts the number of words used in the content.
        """
        return len(strip_tags(self.html_content).split())

    class Meta:
        abstract = True


class ApiBaseModel(models.Model):
    date_created = models.DateTimeField(default=lambda *args: timezone.now())
    date_updated = models.DateTimeField(default=lambda *args: timezone.now())

    @property
    def tags(self):
        return Tag.objects.get_for_object(self)

    class Meta(object):
        abstract = True