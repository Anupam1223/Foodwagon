from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Categories, Product, Offer
from .forms import ProductAddForm, CategoryAddForm
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
                product_in_trader = Product.objects.filter(trader=verifyUser)
                trader = verifyUser

                name = productaddform.cleaned_data["name"]
                for products in product_in_trader:
                    if products.name == name:
                        messages.error(request, "product already exists")
                        return HttpResponseRedirect("/product/productadd")

                quantity = productaddform.cleaned_data["quantity"]
                stock = productaddform.cleaned_data["stock"]
                price = productaddform.cleaned_data["price"]
                image = productaddform.cleaned_data["image"]
                category = productaddform.cleaned_data["category"]

                product = Product(
                    name=name,
                    quantity=quantity,
                    stock=stock,
                    price=price,
                    image=image,
                    trader=trader,
                    category=category,
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

        productstatus = Product.objects.filter(id=id).first()
        if productstatus.status == True:
            Product.objects.filter(id=id).update(status=False)
            messages.success(request, "product disabled")
            return HttpResponseRedirect("/product/productread")
        else:
            Product.objects.filter(id=id).update(status=True)
            messages.success(request, "product activated")
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
        offertime = request.POST.get("validtime")

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
                offer_time=offertime,
            )
            offer.save()
            messages.success(request, "product offer added sucessfully")
            return HttpResponseRedirect("/product/productread")
        else:
            messages.error(request, "product offer aborted, add offer amount")
            return HttpResponseRedirect("/product/productread")


def edit_offer(request):
    if request.method == "POST":

        offer = request.POST.get("offerAmount")
        offer_id = request.POST.get("product_offer")
        offertime = request.POST.get("validtime")

        if offer and offer_id and offertime:
            offerr = Offer.objects.filter(id=offer_id).first()
            offerr.offer_amount = offer
            offerr.offer_time = offertime
            offerr.save()
            messages.success(request, "product offer updated sucessfully")
            return HttpResponseRedirect("/product/productread")
        elif offer and offer_id:
            offerr = Offer.objects.filter(id=offer_id).first()
            offerr.offer_amount = offer
            offerr.save()
            messages.success(request, "product offer updated sucessfully")
            return HttpResponseRedirect("/product/productread")
        else:
            messages.error(request, "product offer aborted, add new offer amount")
            return HttpResponseRedirect("/product/productread")


# Create your views here.
def add_category(request):
    if request.session.has_key("user"):
        if request.method == "POST":
            categoryaddform = CategoryAddForm(
                data=(request.POST or None), files=(request.FILES or None)
            )
            if categoryaddform.is_valid():
                name = categoryaddform.cleaned_data["name"]

                categories = Categories.objects.filter(name=name)
                for category in categories:
                    if category.name == name:
                        messages.error(request, "category already exists")
                        return HttpResponseRedirect("/product/viewcategory")

                name = categoryaddform.cleaned_data["name"]

                category = Categories(
                    name=name,
                )
                category.save()

                messages.success(request, "product added sucessfully")
                return HttpResponseRedirect("/product/viewcategory")
            else:
                print("invalid form")
        else:
            productaddform = CategoryAddForm()
    else:
        return HttpResponseRedirect("../../login/")

    return render(request, "admin/categoryadd.html", {"form": productaddform})


class category_view(TemplateView):
    template_name = "admin/viewcategory.html"

    def get(self, request):

        category = Categories.objects.all()
        return render(request, self.template_name, {"category": category})


def update_category(request, id):
    if request.method == "POST":
        datas = Categories.objects.get(pk=id)
        fm = CategoryAddForm(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )
        if fm.is_valid():
            fm.save()
            messages.success(request, "category updated")
            return HttpResponseRedirect("/product/viewcategory")
        else:
            return render(request, "admin/updatecategory.html", {"forms": fm})

    data = Categories.objects.get(pk=id)
    fm = CategoryAddForm(instance=data)

    return render(request, "admin/updatecategory.html", {"forms": fm})


def delete_category(request, id):
    if request.method == "POST":

        categorystatus = Categories.objects.filter(id=id).first()
        if categorystatus.status == True:
            Categories.objects.filter(id=id).update(status=False)
            messages.success(request, "category disabled")
            return HttpResponseRedirect("/product/viewcategory")
        else:
            Categories.objects.filter(id=id).update(status=True)
            messages.success(request, "category activated")
            return HttpResponseRedirect("/product/viewcategory")
