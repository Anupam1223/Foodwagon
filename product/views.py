from collections import UserList
from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product, Offer
from .forms import ProductAddForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User as users


# Create your views here.
def ProductAdd(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            productaddform = ProductAddForm(
                data=(request.POST or None), files=(request.FILES or None)
            )
            if productaddform.is_valid():

                semail = request.session["user"]
                verifyUser = users.objects.filter(email=semail).first()
                trader = verifyUser
                name = productaddform.cleaned_data["name"]
                quantity = productaddform.cleaned_data["quantity"]
                stock = productaddform.cleaned_data["stock"]
                price = productaddform.cleaned_data["price"]
                image = productaddform.cleaned_data["image"]

                product = Product(
                    name=name,
                    quantity=quantity,
                    stock=stock,
                    price=price,
                    image=image,
                    trader=trader,
                )
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
            offer = Offer.objects.all()
            return render(
                request, self.template_name, {"product": product, "offer": offer}
            )
        else:
            id = verifyUser.id
            product = Product.objects.filter(trader=id)
            offer = Offer.objects.filter(trader_offer=id)
            return render(
                request, self.template_name, {"product": product, "offer": offer}
            )


def delete_product(request, id):
    if request.method == "POST":
        data = Product.objects.get(pk=id)
        data.delete()
        messages.success(request, "product deleted")
        return HttpResponseRedirect("/product/productread")


def delete_offer(request, id):
    if request.method == "POST":
        data = Offer.objects.get(pk=id)
        data.delete()
        messages.success(request, "offer deleted")
        return HttpResponseRedirect("/product/productread")


def update_product(request, id):
    if request.method == "POST":
        datas = Product.objects.get(pk=id)
        fm = ProductAddForm(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )
        if fm.is_valid():
            fm.save()
            messages.success(request, "product updated")
            return HttpResponseRedirect("../productread")
        else:
            return render(request, "admin/updateproduct.html", {"forms": fm})

    data = Product.objects.get(pk=id)
    fm = ProductAddForm(instance=data)

    return render(request, "admin/updateproduct.html", {"forms": fm})


# code for adding offer to product
def add_offer(request):
    if request.method == "POST":

        offer = request.POST.get("offerAmount")
        product = request.POST.get("product_offer")

        if offer and product:
            # extract session value to extract the user password from database
            semail = request.session["user"]

            # extract the user with matching email taken from session
            trader_instance = users.objects.filter(email=semail).first()
            product_instance = Product.objects.filter(id=product).first()

            offer = Offer(
                offer_amount=offer,
                product_offer=product_instance,
                trader_offer=trader_instance,
            )
            offer.save()
            messages.success(request, "product offer added sucessfully")
            return HttpResponseRedirect("/product/productread")
        else:
            messages.error(request, "add offer amount")
            return HttpResponseRedirect("/product/productread")


def edit_offer(request):
    if request.method == "POST":

        offer = request.POST.get("offerAmount")
        offer_id = request.POST.get("product_offer")

        if offer and offer_id:
            offerr = Offer.objects.filter(id=offer_id).first()
            offerr.offer_amount = offer
            offerr.save()
            messages.success(request, "product offer updated sucessfully")
            return HttpResponseRedirect("/product/productread")
        else:
            messages.error(request, "add new offer amount")
            return HttpResponseRedirect("/product/productread")
