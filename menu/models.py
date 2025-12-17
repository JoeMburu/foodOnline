from django.db import models
from django.core.exceptions import ValidationError
from vendor.models import Vendor
from django.template.defaultfilters import slugify


class Category(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category_name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=100, unique=True)
  description = models.TextField(max_length=250, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:     
     verbose_name = 'Category'
     verbose_name_plural = 'Categories'

  def clean(self):
     self.category_name = self.category_name.capitalize()

     # Example: generate slug from category_name
     self.slug = slugify(self.category_name)

     # Check for duplicate slug (excluding self for updates)
     qs = Category.objects.filter(slug=self.slug)
     if self.pk:
      qs = qs.exclude(pk=self.pk)
     if qs.exists():
      raise ValidationError("Category with this name already exists for this vendor.")
  
  def save(self, *args, **kwargs):
       self.full_clean()  # This will call the clean method
       super().save(*args, **kwargs)
     

   



  def __str__(self):
      return self.category_name
  

class FoodItem(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  food_title = models.CharField(max_length=100)
  slug = models.SlugField(max_length=150, unique=True)
  description = models.TextField(max_length=250, blank=True)
  image = models.ImageField(upload_to='fooditems/')
  price = models.DecimalField(max_digits=8, decimal_places=2)
  is_available = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
     verbose_name = 'FoodItem'
     verbose_name_plural = 'Food items' 

  def __str__(self):
      return self.food_title
