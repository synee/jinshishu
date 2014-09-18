# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models
from liang.modules.api.kits import jsonify
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """

    nickname = models.CharField(max_length=32, null=True, verbose_name=_(u'昵称'))

    def __str__(self):
        return self.nickname or self.username

    @property
    def jsonify(self):
        return jsonify(User.objects.get(pk=self.id))

    @property
    def get_profile(self):
        if not hasattr(self, "profile"):
            profile = Profile()
            profile.user = self
            profile.save()
            self.profile = profile
        return Profile.objects.get(pk=self.profile.id)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'


class Profile(models.Model):
    user = models.OneToOneField(to=User, related_name='profile')
    avatar = models.ImageField(verbose_name=u"头像")
    website = models.URLField(verbose_name=u"个人主页")