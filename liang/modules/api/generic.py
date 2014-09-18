# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin


class SingleObjectTemplateView(SingleObjectTemplateResponseMixin, TemplateView):
    model_class = None

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

    def get(self, request, pk=None, *args,  **kwargs):
        context = self.get_context_data(**kwargs)
        context['obj'] = self.model_class.objects.get(pk=pk)
        return self.render_to_response(context)

