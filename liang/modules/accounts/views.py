# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, FormView, UpdateView
from liang.modules.accounts.forms import BasicForm, RegistrationForm, ProfileForm
from liang.modules.accounts.models import User

INDEX_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = "/home/"


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(INDEX_REDIRECT_URL)
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.data['email'],
            password=form.data['password'],
            email=form.data['email'],
            nickname=form.data['email'].replace("@", "#"),
        )
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class SettingView(TemplateView):
    template_name = 'accounts/setting.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'basic_form': BasicForm(request=self.request, instance=self.request.user),
            'profile_form': ProfileForm(request=self.request, instance=self.request.user.get_profile)
        })
        return super(SettingView, self).get_context_data(**kwargs)


class SettingBasicView(UpdateView):
    form_class = BasicForm
    model = User

    def post(self, request, *args, **kwargs):
        kwargs.update({
            'pk': request.user.pk
        })
        self.kwargs = kwargs
        return super(SettingBasicView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("api_success_call")

