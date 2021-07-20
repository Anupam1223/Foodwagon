from django import forms
from login.models import User

# form to update user
class UserUpdateForm(forms.ModelForm):
    newpassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"name": "newpass1", "placeholder": "re-enter password", "class":"form-control form-control-sm mb-2 newpassword",}
        )
    )

    renewpassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "name": "newpass2",
                "class":"form-control form-control-sm mb-2 renewpassword",
                "placeholder": "re-newpassword",
            }
        )
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "profile_pic",
            "password",
            "address",
        ]
        error_messages = {
            "first_name": {"required": ""},
            "email": {"required": ""},
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm mb-2 firstname",
                    "placeholder": "Name",
                    "name":"username"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control form-control-sm mb-2 email",
                    "placeholder": "email",
                    "name":"email_id"
                }
            ),
            "profile_pic": forms.FileInput(
                attrs={
                    "class": "profile",
                    "name":"image"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Old password",
                    "name": "oldpass",
                    "class":"form-control form-control-sm mb-2 password",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "address",
                    "name": "address",
                    "class":"form-control form-control-sm mb-2",
                }
            ),
        }

class UserUpdateeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "address",
            "profile_pic",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm mb-2 firstname",
                    "placeholder": "Name",
                    "name":"username"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm mb-2",
                    "placeholder": "address",
                    "name":"address"
                }
            ),
            "profile_pic": forms.FileInput(
                attrs={
                    "class": "form-control mb-2 upload-image profile",
                    "name":"image"
                }
            ),
        }

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
