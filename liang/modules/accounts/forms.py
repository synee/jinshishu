# -*- coding: utf-8 -*-
from django import forms
from app.forms.angular_model import NgModelFormMixin
from django.utils.translation import ugettext_lazy as _
from liang.modules.accounts.models import User, Profile


class RegistrationForm(forms.Form):
    email = forms.EmailField(label=u'邮箱', widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _(u"邮箱")}))
    password = forms.CharField(label=u'密码', widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"密码")}))
    password_confirm = forms.CharField(label=u'确认密码', widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _(u"确认密码")}))

    def clean_email(self):
        try:
            User.objects.get(email__iexact=self.data['email'])
        except User.DoesNotExist:
            return self.cleaned_data.get('email')
        raise forms.ValidationError(message=_(u"邮箱已被注册."))
            # self.add_error('email', forms.ValidationError(message=_(u"邮箱已被注册.")))

    def clean_password(self):
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.data['password'] != self.data['password_confirm']:
                return self.add_error('password_confirm', forms.ValidationError(message=_(u"密码不匹配.")))
            else:
                return self.cleaned_data['password']

    def clean(self):
        self.clean_password()
        self.clean_email()
        return self.cleaned_data


class BasicForm(NgModelFormMixin, forms.ModelForm):
    def __init__(self, request=None, **kwargs):
        self.request = request
        super(BasicForm, self).__init__(**kwargs)
        self.fields['email'].widget.attrs.update({
            'ng-disabled': "{{ true }}"
        })

    class Meta:
        model = User
        fields = [
            'nickname',
            'email',
        ]


class ProfileForm(NgModelFormMixin, forms.ModelForm):
    def __init__(self, request=None, **kwargs):
        self.request = request
        super(ProfileForm, self).__init__(**kwargs)

    class Meta:
        model = Profile
        fields = [
            'avatar',
            'website'
        ]
