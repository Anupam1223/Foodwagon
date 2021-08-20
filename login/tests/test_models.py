from django.test import TestCase
from login.models import User


class VendorInfoTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(first_name="Big", last_name="Bob")

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_date_of_last_login(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("last_login").verbose_name
        self.assertEqual(field_label, "last login")

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 30)
