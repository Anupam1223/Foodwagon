from django import forms
from .models import Categories, Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "quantity", "stock", "price", "image", "category"]
        error_messages = {
            "name": {"required": ""},
            "quantity": {"required": ""},
            "stock": {"required": ""},
            "price": {"required": ""},
            "image": {"required": "please provide image"},
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "quantity",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "stock",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "price",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        name = self.cleaned_data.get("name", None)
        if not name:
            raise forms.ValidationError("please provide product name", code="invalid")

        quantity = self.cleaned_data.get("quantity", None)
        if not quantity:
            raise forms.ValidationError("please provide quantity", code="invalid")

        stock = self.cleaned_data.get("stock", None)
        if not stock:
            raise forms.ValidationError("please provide stock", code="invalid")

        price = self.cleaned_data.get("price", None)
        if not price:
            raise forms.ValidationError("please provide price", code="invalid")


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name"]
        error_messages = {
            "name": {"required": ""},
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        name = self.cleaned_data.get("name", None)
        if not name:
            raise forms.ValidationError("please provide product name", code="invalid")
