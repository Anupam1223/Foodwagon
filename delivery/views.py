from django.shortcuts import render
from django.views.generic.base import TemplateView
from login.models import User
from product.models import Categories, Product
from product.models import Offer
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

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
        trader = traders[0:4]
        offerss = Offer.objects.all()
        offer = offerss[0:4]
        product1 = product[0:5]
        product2 = product[5:10]

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
        return render(
            request,
            "delivery/vendors.html",
            {
                "trader": page_obj,
                "product": product,
                "total_trader": total_trader_count,
                "category": category,
                "offer": offer,
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
        product = Product.objects.filter(trader_id=id)
        total_trader_count = product.count()

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
                "trader": page_obj,
                "product": product,
                "total_trader": total_trader_count,
                "category": category,
                "offer": offer,
            },
        )
