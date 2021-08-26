from django.test import Client, TestCase
from django.urls import reverse
from login.models import User, VendorInfo
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse("login:signin")
        self.register_url = reverse("login:register")

    def test_loginUser_GET(self):
        response = self.client.get(self.signin_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "sign_in.html")

    def test_UserRegister_GET(self):
        response = self.client.get(self.register_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "sign_up.html")
