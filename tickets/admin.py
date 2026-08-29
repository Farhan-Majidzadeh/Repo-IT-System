from django.contrib import admin
from .models import TicketCategory, Assignment, Ticket, TicketMessage

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'level', 'path')
    search_fields = ('title', 'path')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'category', 'responsible_person', 'is_active')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'status', 'priority', 'assigned_to', 'created_at')
    search_fields = ('code', 'title')
    list_filter = ('status', 'priority', 'category')

@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'message_type', 'created_at')
