from django import forms
from .models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "quantity", "stock", "price"]
        error_messages = {
            "name": {"required": "please enter product name"},
            "quantity": {"required": "please enter quantity"},
            "stock": {"required": "please enter stock"},
            "price": {"required": "please enter price"},
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "please enter total quantity",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "please enter total stock",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "please enter price",
                }
            ),
        }
