from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product
from .forms import ProductAddForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User as users

# Create your views here.
def ProductAdd(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            productaddform = ProductAddForm(data=(request.POST or None), files=(request.FILES or None))
            if productaddform.is_valid():

                semail = request.session["user"]
                verifyUser = users.objects.filter(email=semail).first()
                trader = verifyUser
                name = productaddform.cleaned_data["name"]
                quantity = productaddform.cleaned_data["quantity"]
                stock = productaddform.cleaned_data["stock"]
                price = productaddform.cleaned_data["price"]
                image = productaddform.cleaned_data["image"]

                product = Product(name=name, quantity=quantity, stock=stock, price=price, image=image, trader=trader)
                product.save()

                messages.success(request, "product added sucessfully")
                return HttpResponseRedirect("/product/productread")
            else:
                print("invalid form")
        else:
            productaddform = ProductAddForm()
    else:
        return HttpResponseRedirect("../../login/")

    return render(request, "admin/productadd.html", {"form": productaddform})


class ProductView(TemplateView):
    template_name = "admin/productread.html"

    def get(self, request):

        semail = request.session["user"]
        verifyUser = users.objects.filter(email=semail).first()
        if verifyUser.admin:
            product = Product.objects.all()
            return render(request, self.template_name, {"product": product})
        else:
            id = verifyUser.id
            product = Product.objects.filter(trader=id)
            return render(request, self.template_name, {"product": product})


def delete_product(request, id):
    if request.method == "POST":
        data = Product.objects.get(pk=id)
        data.delete()
        messages.success(request, "product deleted")
        return HttpResponseRedirect("../../productread")


def update_product(request, id):
    if request.method == "POST":
        data = Product.objects.get(pk=id)
        fm = ProductAddForm(data=(request.POST or None), files=(request.FILES or None))
        if fm.is_valid():
            fm.save()
            messages.success(request, "product updated")
            return HttpResponseRedirect("../productread")
        else:
            return render(request, "admin/updateproduct.html", {"forms": fm})
        
    data = Product.objects.get(pk=id)
    fm = ProductAddForm(instance=data)

    return render(request, "admin/updateproduct.html", {"forms": fm})
