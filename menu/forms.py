from django import forms
from menu.models import Category, FoodItem
from vendor.models import Vendor  
# from accounts.validators import allow_only_images_validator


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'image', 'price']
    
    def __init__(self, *args, vendor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(vendor=vendor)
      

