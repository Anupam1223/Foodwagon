from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product
from .forms import ProductAddForm
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def ProductAdd(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            productaddform = ProductAddForm(request.POST)
            if productaddform.is_valid():

                productadd = productaddform.save(commit=False)
                productadd.save()
                messages.success(request, "product added sucessfully")
                return HttpResponseRedirect("/product/productread")
            else:
                print("invalid form")
        else:
            productaddform = ProductAddForm()
    else:
        return HttpResponseRedirect("../../login/")

    return render(request, "productadd.html", {"form": productaddform})


class ProductView(TemplateView):
    template_name = "productread.html"

    def get(self, request):

        product = Product.objects.all()
        return render(request, self.template_name, {"product": product})


def delete_product(request, id):
    if request.method == "POST":
        data = Product.objects.get(pk=id)
        print(data)
        print("hello")
        data.delete()
        messages.success(request, "product deleted")
        return HttpResponseRedirect("../../productread")


def update_product(request, id):
    if request.method == "POST":
        data = Product.objects.get(pk=id)
        fm = ProductAddForm(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
            messages.success(request, "product updated")
            return HttpResponseRedirect("../productread")
    data = Product.objects.get(pk=id)
    fm = ProductAddForm(instance=data)

    return render(request, "updateproduct.html", {"forms": fm})
