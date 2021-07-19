from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.


class CategoryView(TemplateView):
    template_name = "delivery.html"

    def get(self, request):

        return render(request, self.template_name)
