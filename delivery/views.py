from django.shortcuts import render
from django.views.generic.base import TemplateView
from login.models import User, VendorInfo
from product.models import Categories, Product
from product.models import Offer
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
class CategoryView(TemplateView):
    template_name = "delivery.html"

    def get(self, request):

        if request.session.has_key("user"):
            # extract session value to extract the user password from database
            semail = request.session["user"]

            # extract the user with matching email taken from session
            verifyUser = User.objects.filter(email=semail).first()
            if verifyUser.admin or verifyUser.is_staff:
                return HttpResponseRedirect("../admins/admin")

        # return render(request, self.template_name, {'product':product})
        product = Product.objects.all()
        traders = User.objects.filter(is_staff=True, is_active=True)
        print(traders)
        trader = traders[0:4]
        offerss = Offer.objects.all()
        offer = offerss[0:4]
        product1 = product[0:5]
        product2 = product[5:10]
        if request.session.has_key("cart_count"):
            no_of_item_in_cart = request.session["cart_count"]
        else:
            no_of_item_in_cart = None

        return render(
            request,
            self.template_name,
            {
                "trader": trader,
                "product": product,
                "offer": offer,
                "product1": product1,
                "product2": product2,
                "traderss": traders,
                "cart_count": no_of_item_in_cart,
            },
        )


def filter_category(request):
    if request.method == "POST":

        categoryid = request.POST.get("categoryid")
        offerid = request.POST.get("offerid")

        if categoryid == "all" or offerid == "all":
            trader = User.objects.filter(is_staff=True, is_active=True).order_by("id")
            selected_category = None
            total_trader_count = trader.count()
        else:
            traders = []
            if categoryid:
                selected_category = Categories.objects.filter(id=categoryid).first()
                products = Product.objects.filter(category=categoryid)
                for product in products:
                    traders.append(product.trader)
            else:
                selected_category = Offer.objects.filter(id=offerid).first()
                offersss = Offer.objects.filter(id=offerid)
                for product in offersss:
                    traders.append(product.trader_offer)
            trade = set(traders)
            trader = list(trade)

            count = 0
            for traders in trader:
                count = count + 1
            total_trader_count = count
        # paginaton code--------------------------
        paginator = Paginator(trader, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # ----------------------------------------
        category = Categories.objects.all()
        offerss = Offer.objects.all()
        offer = offerss[0:4]
        return render(
            request,
            "delivery/vendors.html",
            {
                "trader": page_obj,
                "category": category,
                "offer": offer,
                "selected_category": selected_category,
                "total_trader": total_trader_count,
            },
        )
    else:
        product = Product.objects.all()
        trader = User.objects.filter(is_staff=True, is_active=True).order_by("id")
        total_trader_count = trader.count()
        category = Categories.objects.all()
        offerss = Offer.objects.all()
        offer = offerss[0:4]
        # paginaton code--------------------------
        paginator = Paginator(trader, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # ----------------------------------------
        if request.session.has_key("cart_count"):
            no_of_item_in_cart = request.session["cart_count"]
        else:
            no_of_item_in_cart = None
        return render(
            request,
            "delivery/vendors.html",
            {
                "trader": page_obj,
                "product": product,
                "total_trader": total_trader_count,
                "category": category,
                "offer": offer,
                "cart_count": no_of_item_in_cart,
            },
        )


def filter_product(request, id):
    if request.method == "POST":

        categoryid = request.POST.get("categoryid")
        offerid = request.POST.get("offerid")

        if categoryid == "all" or offerid == "all":
            trader = User.objects.filter(is_staff=True, is_active=True).order_by("id")
            selected_category = None
            total_trader_count = trader.count()
        else:
            traders = []
            if categoryid:
                selected_category = Categories.objects.filter(id=categoryid).first()
                products = Product.objects.filter(category=categoryid)
                for product in products:
                    traders.append(product.trader)
            else:
                selected_category = Offer.objects.filter(id=offerid).first()
                offersss = Offer.objects.filter(id=offerid)
                for product in offersss:
                    traders.append(product.trader_offer)
            trade = set(traders)
            trader = list(trade)

            count = 0
            for traders in trader:
                count = count + 1
            total_trader_count = count
        # paginaton code--------------------------
        paginator = Paginator(trader, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # ----------------------------------------
        category = Categories.objects.all()
        offerss = Offer.objects.all()
        offer = offerss[0:4]
        return render(
            request,
            "delivery/productpage.html",
            {
                "trader": page_obj,
                "category": category,
                "offer": offer,
                "selected_category": selected_category,
                "total_trader": total_trader_count,
            },
        )
    else:

        sort = request.GET.get("sort")
        print(sort)
        if sort:
            product = Product.objects.filter(trader_id=id).order_by(sort)
        else:
            product = Product.objects.filter(trader_id=id)
        total_trader_count = product.count()
        user = VendorInfo.objects.filter(user_id=id).first()
        trader = User.objects.filter(id=id).first()
        if request.session.has_key("cart_count"):
            no_of_item_in_cart = request.session["cart_count"]
        else:
            no_of_item_in_cart = None
        # paginaton code--------------------------
        paginator = Paginator(product, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        # ----------------------------------------

        category = Categories.objects.all()
        offer = Offer.objects.all()

        return render(
            request,
            "delivery/productpage.html",
            {
                "product": page_obj,
                "user_info": user,
                "total_trader": total_trader_count,
                "category": category,
                "offer": offer,
                "trader": trader,
                "cart_count": no_of_item_in_cart,
            },
        )


def add_to_cart(request):
    if not request.session.has_key("user"):
        data = {"error": "login"}
        return JsonResponse(data)

    if request.method == "GET":
        p_id = request.GET.get("addCart")
        if p_id:
            if request.session.has_key("cart_content"):
                cart = request.session["cart_content"]
            else:
                cart = []

            cart.append(p_id)
            ucart = set(cart)
            user_cart = list(ucart)
            count = 0
            for no_of_element in user_cart:
                count = count + 1
            total_element_count = count
            request.session["cart_count"] = total_element_count
            request.session["cart_content"] = user_cart
            data = {"sucess": total_element_count}
            return JsonResponse(data)


def cart(request):
    if request.method == "POST":
        pass
    else:
        if request.session.has_key("cart_content"):
            product_objects = []
            cart_values = request.session["cart_content"]

            for values in cart_values:
                product = Product.objects.filter(id=values).first()
                product_objects.append(product)
            offer = Offer.objects.all()
            paginator = Paginator(product_objects, 4)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            if request.session.has_key("cart_count"):
                no_of_item_in_cart = request.session["cart_count"]
            else:
                no_of_item_in_cart = None

            return render(
                request,
                "delivery/cartpage.html",
                {
                    "product": page_obj,
                    "offer": offer,
                    "cart_count": no_of_item_in_cart,
                },
            )
        else:
            if request.session.has_key("user"):
                user = request.session["user"]
            else:
                user = None
            return render(
                request,
                "delivery/cartpage.html",
                {
                    "user": user,
                },
            )


def remove_from_cart(request):
    if request.method == "GET":
        p_id = request.GET.get("removeCartItem")
        if p_id:
            items_in_cart = request.session["cart_content"]
            cart = list(items_in_cart)
            cart.remove(p_id)
            count = 0
            for no_of_element in cart:
                count = count + 1
            total_element_count = count
            del request.session["cart_count"]
            del request.session["cart_content"]
            request.session["cart_count"] = total_element_count
            request.session["cart_content"] = cart
            data = {"sucess": total_element_count}
            return JsonResponse(data)
