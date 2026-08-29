from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'start_date', 'end_date', 'status')
    search_fields = ('code', 'name')
