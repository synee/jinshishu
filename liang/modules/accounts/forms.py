# -*- coding: utf-8 -*-
from django import forms
from app.forms.angular_model import NgModelFormMixin
from django.utils.translation import ugettext_lazy as _
from liang.modules.accounts.models import User, Profile


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'maxlength': 60, 'class': 'form-control', 'placeholder': _("Email Address")}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Password")}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'maxlength': 30, 'class': 'form-control', 'placeholder': _("Confirm your password")}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if self.errors:
            for f_name in self.fields:
                if f_name in self.errors:
                    classes = self.fields[f_name].widget.attrs.get('class', '')
                    classes += ' has-error'
                    self.fields[f_name].widget.attrs['class'] = classes

    def clean_email(self):
        try:
            User.objects.get(email__iexact=self.data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_("邮箱已被注册."))

    def clean_password(self):
        if 'password' in self.data and 'password_confirm' in self.data:
            if self.data['password'] != self.data['password_confirm']:
                raise forms.ValidationError(_("密码不匹配."))
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
