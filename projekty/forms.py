from django import forms
from django.contrib.auth.models import User

class MakeProfile(forms.Form):
  username = forms.CharField(max_length=100)
  password = forms.CharField(max_length=100, widget=forms.PasswordInput)
  meno = forms.CharField(max_length=100)
  priezvisko = forms.CharField(max_length=100)
  email = forms.EmailField(widget=forms.EmailInput)

  def clean_username(self):
    username = self.cleaned_data['username']
    if User.objects.filter(username=username):
      raise forms.ValidationError("Používateľské meno už existuje, prosím zvoľte si iné")
    return username
