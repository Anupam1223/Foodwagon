from django import forms
from .models import Categories, Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "image", "category"]
        error_messages = {
            "name": {"required": ""},
            "price": {"required": ""},
            "image": {"required": ""},
            "category": {"required": ""},
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "price",
                }
            ),
            "category": forms.Select(
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

        price = self.cleaned_data.get("price", None)
        if not price:
            raise forms.ValidationError("please provide price", code="invalid")

        image = self.cleaned_data.get("image", None)
        if not image:
            raise forms.ValidationError("please provide image", code="invalid")

        category = self.cleaned_data.get("category", None)
        if not category:
            raise forms.ValidationError("please provide category", code="invalid")


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
