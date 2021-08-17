from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Categories, Product, Offer
from .forms import ProductAddForm, CategoryAddForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User as users
from django.core.paginator import Paginator

# Create your views here.

# -- when admin adds product, with all the information data is brought to this url via POST method
def ProductAdd(request):
    if request.session.has_key("user"):
        # -- if user submit the form this condition will work
        if request.method == "POST":
            # -- instance of ProductAddForm, because our form is created inside forms.py
            productaddform = ProductAddForm(
                data=(request.POST or None), files=(request.FILES or None)
            )

            # -- if all the data given in the form is valid then this condition will pass
            if productaddform.is_valid():

                # -- logged in user is saved in trader database
                semail = request.session["user"]
                verifyUser = users.objects.filter(email=semail).first()
                product_in_trader = Product.objects.filter(trader=verifyUser)
                trader = verifyUser

                # -- all the information of product, i.e name, price, image and category is saved
                name = productaddform.cleaned_data["name"]
                for products in product_in_trader:
                    if products.name == name:
                        messages.error(request, "product already exists")
                        return HttpResponseRedirect("/product/productadd")

                price = productaddform.cleaned_data["price"]
                image = productaddform.cleaned_data["image"]
                category = productaddform.cleaned_data["category"]

                # -- object pf product, with all the values to be stored
                product = Product(
                    name=name,
                    price=price,
                    image=image,
                    trader=trader,
                    category=category,
                )
                # -- this object is saved with all the above data
                product.save()

                messages.success(request, "product added sucessfully")
                return HttpResponseRedirect("/product/productread")
            else:
                print("invalid form")
        # -- if user is just viewing the Add Product page, i.e get method
        else:
            productaddform = ProductAddForm()
    else:
        # -- if user is not logged-in then it is redirected to login page
        return HttpResponseRedirect("../../login/")

    return render(request, "admin/productadd.html", {"form": productaddform})


class ProductView(TemplateView):
    # -- template that will be shown when hitting this url
    template_name = "admin/productread.html"

    def get(self, request):
        # -- we are checking whether the user is admin or restaurent owner
        semail = request.session["user"]
        verifyUser = users.objects.filter(email=semail).first()

        # -- if user is admin then we should show all the product
        if verifyUser.admin:
            product = Product.objects.all()
            offer = Offer.objects.all()

            # ------------- Pagination Code --------------------
            paginator = Paginator(product, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            # ---------------------------------------------------

            # -- template is rendered with additional context(product, product_offer, offer)
            return render(
                request,
                self.template_name,
                {"product": page_obj, "product_offer": product, "offer": offer},
            )
        # -- if the user is restaurent ownner, then he/she will only see the product of their restaurent
        else:
            id = verifyUser.id
            product = Product.objects.filter(trader=id)
            offer = Offer.objects.filter(trader_offer=id)

            # ------------- Pagination Code --------------------
            paginator = Paginator(product, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            # ---------------------------------------------------
            # -- template is rendered with additional context(product, product_offer, offer)
            return render(
                request,
                self.template_name,
                {"product": page_obj, "product_offer": product, "offer": offer},
            )


# -- we hit this url to disable the product
def delete_product(request, id):
    if request.method == "POST":

        # -- first we get the status of the product
        productstatus = Product.objects.filter(id=id).first()

        # -- if the product is available then we disable it, when this url is hit
        if productstatus.status == True:
            Product.objects.filter(id=id).update(status=False)
            messages.success(request, "product disabled")
            return HttpResponseRedirect("/product/productread")

        # -- if the product is available then we disable it, when this url is hit
        else:
            Product.objects.filter(id=id).update(status=True)
            messages.success(request, "product activated")
            return HttpResponseRedirect("/product/productread")


# -- we hit this url to delete offer
def delete_offer(request, id):

    # -- when we click delete offer logo, then this condition will run return
    # -- httpresponse with message
    if request.method == "POST":
        data = Offer.objects.get(pk=id)
        data.delete()
        messages.success(request, "offer deleted")
        return HttpResponseRedirect("/product/productread")


# -- we hit this url to update product
def update_product(request, id):
    # -- if we click update button from template to update the data of product
    if request.method == "POST":
        datas = Product.objects.get(pk=id)
        fm = ProductAddForm(
            data=(request.POST or None), files=(request.FILES or None), instance=datas
        )
        # -- if user provides valid data then this condition is passed
        if fm.is_valid():

            # -- data is saved with success message in productread
            fm.save()
            messages.success(request, "product updated")
            return HttpResponseRedirect("../productread")

        # -- if user is not valid error-message will be shown
        else:
            return render(request, "admin/updateproduct.html", {"forms": fm})
    # -- template will be rendered without any post data
    data = Product.objects.get(pk=id)
    fm = ProductAddForm(instance=data)

    return render(request, "admin/updateproduct.html", {"forms": fm})


# -- code for adding offer to product
def add_offer(request):
    # -- when admin or super-admin click update button to add offer to the product
    # -- this method is entered
    if request.method == "POST":
        # -- all the post data send from offer modal
        offer = request.POST.get("offerAmount")
        product = request.POST.get("product_offer")
        offertime = request.POST.get("validtime")

        if offer and product:
            # extract session value to extract the user email from database
            semail = request.session["user"]

            # extract the user with matching email taken from session
            trader_instance = users.objects.filter(email=semail).first()
            product_instance = Product.objects.filter(id=product).first()

            # -- creating offer object to save all the data regarding offer
            offer = Offer(
                offer_amount=offer,
                product_offer=product_instance,
                trader_offer=trader_instance,
                offer_time=offertime,
            )
            # -- saves offer with success message sent with message.success
            offer.save()
            messages.success(request, "product offer added sucessfully")
            return HttpResponseRedirect("/product/productread")

        # -- if user doesnt provide offer amount or product
        else:
            messages.error(request, "product offer aborted, add offer amount")
            return HttpResponseRedirect("/product/productread")


# -- we hit this url to update offer
def edit_offer(request):
    if request.method == "POST":
        # -- all the post data send from offer modal to update offer
        offer = request.POST.get("offerAmount")
        offer_id = request.POST.get("product_offer")
        offertime = request.POST.get("validtime")

        # -- if all the valid data is provided
        if offer and offer_id and offertime:

            # -- filters out which product is to be updated
            offerr = Offer.objects.filter(id=offer_id).first()
            offerr.offer_amount = offer
            offerr.offer_time = offertime
            # -- saves the object with data provided by user
            offerr.save()
            # -- success message is send if offer is updated successfully
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
