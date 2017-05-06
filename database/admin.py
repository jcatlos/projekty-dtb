from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('title', 'consultant', 'oponent', 'registration_date')
  list_filter = ('registration_date',)
  search_fields = ('title', 'authors', 'consultant', 'oponent')
  date_hierarchy = 'registration_date'
  ordering = ('-registration_date',)
  fields = ('title', 'authors', 'consultant', 'oponent')
  filter_horizontal = ('authors',)


admin.site.register(Project, ProjectAdmin)

