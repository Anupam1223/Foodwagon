from django.shortcuts import render
from django.views.generic.base import TemplateView
from login.models import User
from product.models import Product
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

        product = Product.objects.all()
        #trader = User.objects.filter(is_staff=True)

        return render(request, self.template_name, {'product':product})
