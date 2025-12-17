from django import forms
from menu.models import Category
# from vendor.models import Vendor  
# from accounts.validators import allow_only_images_validator


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']