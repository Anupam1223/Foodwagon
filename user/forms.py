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
                    "class": "form-control mb-2 upload-image profile",
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
        }

class UserUpdateeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "email",
            "profile_pic",
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
                    "class": "form-control mb-2 upload-image profile",
                    "name":"image"
                }
            ),
        }
