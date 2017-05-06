from django import forms
from database.models import Project, Document
from django.contrib.auth.models import User
import os


class ZmenProjekt(forms.Form):
  nazov = forms.CharField()
  konzultant = forms.CharField()
  autor1 = forms.CharField()
  autor2 = forms.CharField(required = False)
  autor3 = forms.CharField(required = False)
  popis = forms.CharField(required = False, widget=forms.Textarea)

  def clean_konzultant(self):
    konzultant = self.cleaned_data['konzultant']
    try:
      User.objects.get(username=konzultant)
    except User.DoesNotExist:
      raise forms.ValidationError("Konzultant s týmto používateľským menom neexistuje")
    else:
      return konzultant

  def clean_autor1(self):
    autor1 = self.cleaned_data['autor1']
    try:
      User.objects.get(username=autor1)
    except User.DoesNotExist:
      raise forms.ValidationError("Autor s týmto používateľským menom neexistuje")
    else:
      return autor1

  def clean_autor2(self):
    if not self.cleaned_data['autor2'] == "":
      autor2 = self.cleaned_data['autor2']
      try:
        clovek=User.objects.get(username=autor2)
      except User.DoesNotExist:
        raise forms.ValidationError("Autor s týmto používateľským menom neexistuje")
      else:
        return autor2

  def clean_autor3(self):
    if self.cleaned_data['autor3']:
      autor3 = self.cleaned_data['autor3']
      try:
        User.objects.get(username=autor3)
      except User.DoesNotExist:
        raise forms.ValidationError("Autor s týmto používateľským menom neexistuje")
      else:
        return autor3


class PridajDokument(forms.Form):
  projekt = forms.FileField()

  def clean_projekt(self):
    projekt=self.cleaned_data['projekt']
    ext = os.path.splitext(projekt.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.odt', '.txt']
    if not ext.lower() in valid_extensions:
        raise forms.ValidationError(u'Nepodporovaná prípona súboru')
