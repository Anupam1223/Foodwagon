from django import forms
from login.models import User

# form to add user
class AdminAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "address",
            "email",
            "first_name",
            "last_name",
            "password",
            "profile_pic",
            "is_active",
            "is_staff",
            "admin",
        ]
        error_messages = {
            "first_name": {"required": ""},
            "last_name": {"required": ""},
            "email": {"required": ""},
            "password": {"required": ""},
        }
        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control password",
                    "placeholder": "password",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "address",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "firstname",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "email",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "lastname",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        address = self.cleaned_data.get("address", None)
        if not address:
            raise forms.ValidationError("please provide address", code="invalid")

        first_name = self.cleaned_data.get("first_name", None)
        if not first_name:
            raise forms.ValidationError("please provide firstname", code="invalid")

        last_name = self.cleaned_data.get("last_name", None)
        if not last_name:
            raise forms.ValidationError("please provide lastname", code="invalid")

        email = self.cleaned_data.get("email", None)
        if not email:
            raise forms.ValidationError("please provide email", code="invalid")

        password = self.cleaned_data.get("password", None)
        if not password:
            raise forms.ValidationError("please provide password", code="invalid")

# form to update user
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "address",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "admin",
        ]
        error_messages = {
            "address": {"required": ""},
            "first_name": {"required": ""},
            "last_name": {"required": ""},
            "email": {"required": ""},
        }
        widgets = {
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "address",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "firstname",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "email",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "lastname",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        first_name = self.cleaned_data.get("first_name", None)
        if not first_name:
            print("please provide firstname")
            raise forms.ValidationError("please provide firstname", code="invalid")

        last_name = self.cleaned_data.get("last_name", None)
        if not last_name:
            print("please provide lastname")
            raise forms.ValidationError("please provide lastname", code="invalid")

        email = self.cleaned_data.get("email", None)
        if not email:
            print("please provide email")
            raise forms.ValidationError("please provide email", code="invalid")

        address = self.cleaned_data.get("address", None)
        if not address:
            print("please provide address")
            raise forms.ValidationError("please provide address", code="invalid")