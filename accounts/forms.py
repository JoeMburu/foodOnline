from django import forms
from accounts.models import User


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