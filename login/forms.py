from django import forms
from .models import User

class LoginForm(forms.Form):

    email = forms.EmailField(
        error_messages={"required": ""},
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Email",
                "name": "your_name",
                "id": "your_name",
                "class":"username",
            }
        ),
    )

    password = forms.CharField(
        error_messages={"required": ""},
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "name": "your_password",
                "id": "your_password",
                "class":"password",
            }
        ),
    )
    rememberMe = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                "name": "remember-me",
                "id": "remember-me",
                "class": "agree-term",
            }
        ),
    )


# form to add user
class UserAddForm(forms.ModelForm):
    re_pass = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"id": "re_pass", "placeholder": "re-enter password", "class":"re-password",}
        )
    )

    terms = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={
                "name": "agree-term",
                "id": "agree-term",
                "class": "agree-term",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "password",
        ]
        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "password",
                    "name": "pass",
                    "id": "pass",
                    "class":"form-control form-control-sm mb-2 password",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "firstname",
                    "name": "name",
                    "id": "name",
                    "class":"name",
                    
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "email",
                    "name": "email",
                    "id": "email",
                    "class":"username",
                }
            ),
        }
