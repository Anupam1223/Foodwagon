from django.shortcuts import render
from django.views.generic.base import TemplateView
from login.models import User, VendorInfo
from product.models import Categories, Product
from product.models import Offer
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime as date, timedelta
from .models import Order, Order_details
from uuid import uuid4
import datetime

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
            initial_total = 0

            for values in cart_values:
                product = Product.objects.filter(id=values).first()
                product_objects.append(product)
                initial_total += product.price

            offer = Offer.objects.all()
            paginator = Paginator(product_objects, 4)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            if request.session.has_key("cart_count"):
                no_of_item_in_cart = request.session["cart_count"]
            else:
                no_of_item_in_cart = None
            datenow = date.today().strftime("%A")
            time = date.now().hour
            full_date = date.today().strftime("%B %d, %Y")

            if datenow == "Sunday":
                wed = date.today() + timedelta(days=3)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=4)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=5)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Monday":
                wednesday = date.today() + timedelta(days=2)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=3)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=4)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Tuesday":
                wed = date.today() + timedelta(days=1)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=2)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=3)
                friday = date.strftime(fri, "%Y-%m-%d")

            print("Friday ->", friday)

            if datenow == "Wednesday":
                wednesday = None
                thu = date.today() + timedelta(days=1)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=2)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Thursday":
                wednesday = None
                thursday = None
                fri = date.today() + timedelta(days=1)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Friday":
                wednesday = None
                thursday = None
                fri = date.today()
                friday = date.strftime(fri, "%Y-%m-%d")

            return render(
                request,
                "delivery/cartpage.html",
                {
                    "product": page_obj,
                    "offer": offer,
                    "cart_count": no_of_item_in_cart,
                    "initial_total": int(initial_total),
                    "datenow": datenow,
                    "time": time,
                    "full_date": full_date,
                    "wednesday": wednesday,
                    "thursday": thursday,
                    "friday": friday,
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


def add_to_order(request):
    if request.method == "POST":
        price = request.POST.getlist("price[]")
        quantity = request.POST.getlist("quantity[]")
        product = request.POST.getlist("product[]")

        collectiontime = request.POST.get("collectiontime")
        collectionday = request.POST.get("collectionday")
        address = request.POST.get("address")
        streetaddress = request.POST.get("streetaddress")
        city = request.POST.get("city")
        region = request.POST.get("region")
        postal = request.POST.get("postal")
        country = request.POST.get("country")
        totalprice = request.POST.get("totalprice")

        if collectionday == "none":
            data = {"error": "please select food delivery day"}
            return JsonResponse(data)

        if collectiontime == "none":
            data = {"error": "please select food delivery time"}
            return JsonResponse(data)

        if not address:
            data = {"error": "give your address"}
            return JsonResponse(data)

        if not streetaddress:
            data = {"error": "give your exact address"}
            return JsonResponse(data)

        if not city:
            data = {"error": "give the name of your city"}
            return JsonResponse(data)

        if not region:
            data = {"error": "give the name of the region you live in"}
            return JsonResponse(data)

        if not postal:
            data = {"error": "give the postal code of your city"}
            return JsonResponse(data)

        if not country:
            data = {"error": "name of your country"}
            return JsonResponse(data)

        rand_token = uuid4()
        emailid = request.session["user"]
        user = User.objects.filter(email=emailid).first()

        order = Order()

        order.time = collectiontime
        order.day = collectionday
        order.address = address
        order.streetaddress = streetaddress
        order.city = city
        order.region = region
        order.postal = postal
        order.country = country
        order.total_price = totalprice
        order.user = user
        order.token = rand_token
        order.save()

        orderoo = Order.objects.filter(token=rand_token).first()

        for i in range(len(product)):
            products = product[i]
            productss = Product.objects.filter(id=products).first()

            quantities = quantity[i]
            prices = price[i]
            orders = orderoo

            order_details = Order_details()
            order_details.price = prices
            order_details.quantity = quantities
            order_details.product = productss
            order_details.order = orders
            order_details.save()
        data = {"success": ""}
        return JsonResponse(data)
