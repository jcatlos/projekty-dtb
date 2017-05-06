from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Document(models.Model):
  cas_pridania = models.DateTimeField(default=timezone.now)
  dokument = models.FileField(upload_to=('projekty/%Y/'))


class Project(models.Model):
  title = models.CharField(max_length=100, default='Nepomenovaný projekt')
  description = models.CharField(max_length=1000, blank=True, null=True)
  document = models.OneToOneField(Document, related_name = "document", null=True, blank=True)
  consultant = models.ForeignKey(User, related_name = "consultant", blank=True, null=True)
  authors = models.ManyToManyField(User, related_name = "projects")
  oponent = models.ForeignKey(User, related_name = "oponent", null=True)
  registration_date = models.DateField(default=timezone.now)

  def __str__(self):
    return self.title



