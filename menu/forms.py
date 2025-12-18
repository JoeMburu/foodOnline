from django import forms
from accounts.validators import allow_only_images_validator
from menu.models import Category, FoodItem
from vendor.models import Vendor  



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w100'}), validators=[allow_only_images_validator])  # , validators=[allow_only_images_validator]
    class Meta:
        model = FoodItem
        fields = ['category', 'food_title', 'description', 'image', 'price', 'is_available']
    
    def __init__(self, *args, vendor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(vendor=vendor)
      

