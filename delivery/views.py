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
from decimal import *
from django.http import HttpResponse
from mulberry.utils import render_to_pdf

# Create your views here.

# ----- CategoryView sends all the data from backend to main page -------
class CategoryView(TemplateView):
    template_name = "delivery.html"

    def get(self, request):

        # -- checks if user is logged-in or not, if user is logged in then we can see
        # -- username in the top navigation panel, we can click the name and see the user profile
        if request.session.has_key("user"):
            # extract session value to extract the user password from database
            semail = request.session["user"]

            # extract the user with matching email taken from session
            verifyUser = User.objects.filter(email=semail).first()

            # -- if the user logged in is super-admin or admin then he/she is
            # -- logged in another admin panel
            if verifyUser.admin or verifyUser.is_staff:
                return HttpResponseRedirect("../admins/admin")

        product = Product.objects.all()
        traders = User.objects.filter(is_staff=True, is_active=True)

        # -- just sending only four trader in main panel, after clicking view all we can see all restaurent
        trader = traders[0:4]
        offerss = Offer.objects.all()

        # -- only sending four product with offer
        offer = offerss[0:4]

        # -- sending different lists of for slider
        product1 = product[0:5]
        product2 = product[5:10]

        # -- checking whether there is an item in cart, if so show the no of items in cart
        if request.session.has_key("cart_count"):
            no_of_item_in_cart = request.session["cart_count"]
        else:
            no_of_item_in_cart = None

        # -- rendering all the data with the above information as dictionary
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

    # -- if user selects offer or category and search for it
    # -- post data hits this url then this condition will work
    if request.method == "POST":

        # -- for searching according to category
        categoryid = request.POST.get("categoryid")

        # -- for searching according to offer
        offerid = request.POST.get("offerid")

        # -- if all is selected than all the restaurent is shown
        if categoryid == "all" or offerid == "all":
            trader = User.objects.filter(is_staff=True, is_active=True).order_by("id")
            selected_category = None
            total_trader_count = trader.count()
        # -- else only selected restaurent according to category is shown
        else:
            traders = []

            # -- if user wants to search according to category
            if categoryid:
                selected_category = Categories.objects.filter(id=categoryid).first()
                products = Product.objects.filter(category=categoryid)
                # -- trader with only selected category is shown
                for product in products:
                    traders.append(product.trader)

            # -- if user wants to search according to offer
            else:
                selected_category = Offer.objects.filter(id=offerid).first()
                offersss = Offer.objects.filter(id=offerid)
                for product in offersss:
                    traders.append(product.trader_offer)

            # -- converting the list containing trader to set so that same trader wont be saved for two times
            trade = set(traders)
            # -- again converting it to list becuase nopw we have filtered data, and its way easier to work with list
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

        # -- if cart has food than it will show count of food else it will store none
        if request.session.has_key("cart_count"):
            no_of_item_in_cart = request.session["cart_count"]
        else:
            no_of_item_in_cart = None

        # -- to show in the tempalte, so that user can select the category
        category = Categories.objects.all()
        offerss = Offer.objects.all()
        offer = offerss[0:2]

        return render(
            request,
            "delivery/vendors.html",
            {
                "trader": page_obj,
                "category": category,
                "offer": offer,
                "selected_category": selected_category,
                "total_trader": total_trader_count,
                "cart_count": no_of_item_in_cart,
            },
        )
    # -- if user hits the url to show restaurent page than this part of code will send required
    # -- data
    else:
        product = Product.objects.all()
        trader = User.objects.filter(is_staff=True, is_active=True).order_by("id")
        total_trader_count = trader.count()
        category = Categories.objects.all()
        offerss = Offer.objects.all()
        offer = offerss[0:2]

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


# -- when we hit this url we will get filtered restaurents
def filter_product(request, id):
    # -- if
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
        offer = offerss[0:2]
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


# -- we hit this url to add food in cart
def add_to_cart(request):
    # -- if user is not logged-in then he she cannot add food to the cart
    # -- instead a jsonresponse of error is sent
    if not request.session.has_key("user"):
        data = {"error": "login"}
        return JsonResponse(data)

    # -- data or product id is sent from ajax, that product id is catched in a variable
    if request.method == "GET":
        p_id = request.GET.get("addCart")
        if p_id:
            # -- if the cart already contains food then newly selected
            # -- food id is appended to the list cart
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

            # -- cart count, total number of food in cart is saved in session
            request.session["cart_count"] = total_element_count

            # -- cart content, total food in cart is saved in this session
            request.session["cart_content"] = user_cart

            # -- if all the session is saved successully then success response is sent to ajax
            data = {"sucess": total_element_count}
            return JsonResponse(data)


# -- actuall cart page
def cart(request):
    # -- if we are initially viewing the cart
    if request.method == "GET":
        # -- if there is atleast one food in cart then this condition is runned
        if request.session.has_key("cart_content"):

            # -- list to store food in cart
            product_objects = []

            # --accessing cart value so that we can extract all the food selected by user
            cart_values = request.session["cart_content"]
            initial_total = 0

            # -- going through all the values inside of list to save each of them in product_objects
            for values in cart_values:
                product = Product.objects.filter(id=values).first()
                product_objects.append(product)
                initial_total += product.price

            # -- creating a object of Offer table
            offer = Offer.objects.all()

            # -------pagination code -----------------------------
            paginator = Paginator(product_objects, 4)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            # ----------------------------------------------------

            # -- checking if cart contains any food
            # -- if it contains then it is send as a context to template
            if request.session.has_key("cart_count"):
                no_of_item_in_cart = request.session["cart_count"]
            else:
                no_of_item_in_cart = None

            # -- working for time, user need to select date and time of order
            # -- datenow stores todays date
            datenow = date.today().strftime("%A")
            time = date.now().hour

            # -- full_date stores todays date in format -> AUGUST 17, 2021
            full_date = date.today().strftime("%B %d, %Y")

            # -- condition of day, if today is sunday then user can select sun, mon, tue, wed, thu, fri
            if datenow == "Sunday":
                sun = date.today()
                sunday = date.strftime(sun, "%Y-%m-%d")

                mon = date.today() + timedelta(days=1)
                monday = date.strftime(mon, "%Y-%m-%d")

                tue = date.today() + timedelta(days=2)
                tuesday = date.strftime(tue, "%Y-%m-%d")

                wed = date.today() + timedelta(days=3)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=4)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=5)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Monday":

                sunday = None

                mon = date.today()
                monday = date.strftime(mon, "%Y-%m-%d")

                tue = date.today() + timedelta(days=1)
                tuesday = date.strftime(tue, "%Y-%m-%d")

                wed = date.today() + timedelta(days=2)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=3)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=4)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Tuesday":

                sunday = None
                monday = None

                tue = date.today()
                tuesday = date.strftime(tue, "%Y-%m-%d")

                wed = date.today() + timedelta(days=1)
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=2)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=3)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Wednesday":
                sunday = None
                monday = None
                tuesday = None
                wed = date.today()
                wednesday = date.strftime(wed, "%Y-%m-%d")

                thu = date.today() + timedelta(days=1)
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=2)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Thursday":
                sunday = None
                monday = None
                tuesday = None
                wednesday = None

                thu = date.today()
                thursday = date.strftime(thu, "%Y-%m-%d")

                fri = date.today() + timedelta(days=1)
                friday = date.strftime(fri, "%Y-%m-%d")

            if datenow == "Friday":
                sunday = None
                monday = None
                tuesday = None
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
                    "sunday": sunday,
                    "monday": monday,
                    "tuesday": tuesday,
                    "wednesday": wednesday,
                    "thursday": thursday,
                    "friday": friday,
                },
            )
        # -- if user is not logged-in then this data is rendered to cart page
        else:
            if request.session.has_key("user"):
                users = request.session["user"]
                user = User.objects.filter(email=users).first()

            else:
                user = None
            return render(
                request,
                "delivery/cartpage.html",
                {
                    "user": user,
                },
            )


# -- we hit this url if we want to remove food from cart
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

        collectionday = request.POST.get("collectionday")
        address = request.POST.get("address")
        streetaddress = request.POST.get("streetaddress")
        region = request.POST.get("region")
        postal = request.POST.get("postal")
        country = request.POST.get("country")
        totalprice = request.POST.get("totalprice")

        if collectionday == "none":
            data = {"error": "please select food delivery day"}
            return JsonResponse(data)

        if not address:
            data = {"error": "give your address"}
            return JsonResponse(data)

        if not streetaddress:
            data = {"error": "give your exact address"}
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

        emailid = request.session["user"]
        user = User.objects.filter(email=emailid).first()

        order = Order()

        order.day = collectionday
        order.address = address
        order.streetaddress = streetaddress
        order.region = region
        order.postal = postal
        order.country = country
        order.total_price = totalprice
        order.user = user
        order.save()

        for i in range(len(product)):
            products = product[i]
            productss = Product.objects.filter(id=products).first()

            quantities = quantity[i]
            prices = price[i]

            order_details = Order_details()
            order_details.price = prices
            order_details.quantity = quantities
            order_details.product = productss
            order_details.order = order
            order_details.save()

        data = {"success": ""}
        return JsonResponse(data)


class View_Order(TemplateView):
    template_name = "admin/order_view.html"

    def get(self, request):
        semail = request.session["user"]
        verifyUser = User.objects.filter(email=semail).first()

        if verifyUser.admin:
            order = Order.objects.all()

            paginator = Paginator(order, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                self.template_name,
                {"order": page_obj},
            )
        else:
            id = verifyUser.id
            order_details_for_trader = []
            all_order_details = Order_details.objects.all()
            for details in all_order_details:
                if details.product.trader_id == id:
                    order_details_for_trader.append(details.order)

            details_for_trader = set(order_details_for_trader)
            unique_details_for_trader = list(details_for_trader)

            paginator = Paginator(unique_details_for_trader, 5)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                self.template_name,
                {"order": page_obj},
            )


def view_bill(request, id):
    if request.method == "POST":
        pass
    else:
        semail = request.session["user"]
        verifyUser = User.objects.filter(email=semail).first()

        order_id = id
        invoice_data = Order.objects.filter(id=order_id).first()

        if verifyUser.admin:

            vat = []
            service_charge = []
            totals = []
            subtotal = []
            vat_amount = []
            total = 0
            to_pay = 0
            sub_total = 0
            traders = []

            invoice = Order_details.objects.filter(order=order_id)

            for invoc in invoice:
                product = Product.objects.filter(id=invoc.product.id).first()
                restaurent = VendorInfo.objects.filter(
                    user_id=product.trader_id
                ).first()

                total = invoc.price * invoc.quantity
                totals.append(total)
                traders.append(restaurent.user.first_name)

                # if restaurent.additional_vat not in vat:
                vat_amt = (
                    Decimal(restaurent.additional_vat / 100).quantize(
                        Decimal(".01"), rounding=ROUND_DOWN
                    )
                    * invoc.price
                )
                servicecharge = restaurent.additional_service_charge

                vat_amount.append(vat_amt)
                vat.append(restaurent.additional_vat)
                service_charge.append(servicecharge)

                sub_total = total + (vat_amt + Decimal(servicecharge))
                subtotal.append(sub_total)

            for subtotals in subtotal:
                to_pay = to_pay + subtotals

        else:
            traders = None
            individual_invoice = []
            invoices = Order_details.objects.filter(order=order_id)
            for invoc in invoices:
                if invoc.product.trader_id == verifyUser.id:
                    individual_invoice.append(invoc)

            user_extra_info = VendorInfo.objects.filter(user_id=verifyUser.id).first()
            vat = user_extra_info.additional_vat
            service_charge = user_extra_info.additional_service_charge
            invoice = individual_invoice

            subtotal = 0
            for info in invoice:
                subtotal = subtotal + (info.quantity * info.price)

            vat_amount = Decimal(vat / 100).quantize(
                Decimal(".01"), rounding=ROUND_DOWN
            ) * (subtotal)

            to_pay = subtotal + (vat_amount + Decimal(service_charge))
        contexts = {
            "invoice": invoice,
            "invoice_data": invoice_data,
            "vat": vat,
            "vat_amount": vat_amount,
            "service_charge": service_charge,
            "subtotal": subtotal,
            "to_pay": to_pay,
            "subtotal": subtotal,
            "trader": traders,
        }
        return render(request, "admin/invoice.html", contexts)


def generatePDF(request, id):

    if request.method == "GET":
        semail = request.session["user"]

        verifyUser = User.objects.filter(email=semail).first()

        order_id = id
        invoice_data = Order.objects.filter(id=order_id).first()

        if verifyUser.admin:

            vat = []
            service_charge = []
            totals = []
            subtotal = []
            vat_amount = []
            total = 0
            to_pay = 0
            sub_total = 0

            invoice = Order_details.objects.filter(order=order_id)

            for invoc in invoice:
                product = Product.objects.filter(id=invoc.product.id).first()
                restaurent = VendorInfo.objects.filter(
                    user_id=product.trader_id
                ).first()

                total = invoc.price * invoc.quantity
                totals.append(total)

                if restaurent.additional_vat not in vat:
                    vat_amt = (
                        Decimal(restaurent.additional_vat / 100).quantize(
                            Decimal(".01"), rounding=ROUND_DOWN
                        )
                        * invoc.price
                    )
                    servicecharge = restaurent.additional_service_charge

                    vat_amount.append(vat_amt)
                    vat.append(restaurent.additional_vat)
                    service_charge.append(servicecharge)

                sub_total = total + (vat_amt + Decimal(servicecharge))
                subtotal.append(sub_total)

            for subtotals in subtotal:
                to_pay = to_pay + subtotals

        else:
            individual_invoice = []
            invoices = Order_details.objects.filter(order=order_id)
            for invoc in invoices:
                if invoc.product.trader_id == verifyUser.id:
                    individual_invoice.append(invoc)

            user_extra_info = VendorInfo.objects.filter(user_id=verifyUser.id).first()
            vat = user_extra_info.additional_vat
            service_charge = user_extra_info.additional_service_charge
            invoice = individual_invoice

            subtotal = 0
            for info in invoice:
                subtotal = subtotal + (info.quantity * info.price)

            vat_amount = Decimal(vat / 100).quantize(
                Decimal(".01"), rounding=ROUND_DOWN
            ) * (subtotal)

            to_pay = subtotal + (vat_amount + Decimal(service_charge))
        contexts = {
            "invoice": invoice,
            "invoice_data": invoice_data,
            "vat": vat,
            "vat_amount": vat_amount,
            "service_charge": service_charge,
            "subtotal": subtotal,
            "to_pay": to_pay,
            "subtotal": subtotal,
        }
        pdf = render_to_pdf("invoice.html", contexts)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Not found")


def paid(request, id):
    if request.method == "GET":
        order_id = id
        Order.objects.filter(id=order_id).update(status=True)
        return HttpResponseRedirect("../view_bill/" + str(id))
