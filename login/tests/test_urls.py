from django.contrib.auth import login
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from login.views import loginUser

"""
class TestUrls(SimpleTestCase):
    def test_sigin_url_is_resolved(self):
        url = reverse("login:signin")
        self.assertEquals(resolve(url).func, loginUser)"""
