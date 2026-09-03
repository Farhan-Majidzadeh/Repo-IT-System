from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_path'),
    path('assets/', views.asset_report, name='asset_report'),
    path('consumables/', views.consumable_report, name='consumable_report'),
    path('cartridges/', views.cartridge_report, name='cartridge_report'),
    path('referrals/', views.referral_report, name='referral_report'),
    path('tickets/', views.ticket_report, name='ticket_report'),
    path('suppliers/', views.supplier_report, name='supplier_report'),
    path('export/<str:report_type>/', views.export_excel, name='export_excel'),
]
