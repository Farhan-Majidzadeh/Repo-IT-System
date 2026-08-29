from django.contrib import admin
from .models import Department, Personnel, PersonnelDepartment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'building')
    search_fields = ('code', 'name')

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('personnel_code', 'full_name', 'email', 'is_active')
    search_fields = ('personnel_code', 'full_name', 'email')

@admin.register(PersonnelDepartment)
class PersonnelDepartmentAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'department', 'entry_date', 'is_current')
