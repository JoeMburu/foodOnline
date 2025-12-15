from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password'  ]


  def clean(self):
    cleaned_data = super(UserRegistrationForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    username = cleaned_data.get('username')

    if password != confirm_password:
      raise forms.ValidationError(
        "Password and Confirm Password do not match"
      )
    
    # if User.objects.filter(username=username).exists():
    #   raise forms.ValidationError(
    #     "Username already exists"
    #   )
    return cleaned_data

   
class UserProfileForm(forms.ModelForm):
  address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing...','required':'required'}))
  profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
  cover_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator]) 

  latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
  longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

  class Meta:
    model = UserProfile
    fields = ['profile_picture', 'cover_picture', 'address', 'city', 'country', 'post_code', 'longitude', 'latitude']

