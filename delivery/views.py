from django.shortcuts import render
from django.views.generic.base import TemplateView
from login.models import User
from product.models import Product
from product.models import Offer
from django.http import HttpResponseRedirect

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
        traders = User.objects.filter(is_staff=True)
        trader = traders[0:5]
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
            },
        )


class VendorView(TemplateView):
    template_name = "delivery/vendors.html"

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
        trader = User.objects.filter(is_staff=True)
        total_trader_count = trader.count()

        return render(
            request,
            self.template_name,
            {
                "trader": trader,
                "product": product,
                "total_trader": total_trader_count,
            },
        )
