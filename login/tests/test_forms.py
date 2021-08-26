from django.test import TestCase

from login.forms import LoginForm


class LoginFormTests(TestCase):
    def test_email(self):
        form = LoginForm(
            data={
                "email": "anupam@gmail.com",
                "password": "anupam",
                "rememberMe": "True",
            }
        )
        self.assertTrue(form.is_valid())
