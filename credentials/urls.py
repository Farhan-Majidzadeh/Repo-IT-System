from django.urls import path
from . import views

app_name = 'credentials'

urlpatterns = [
    path('api/toggle-password/<int:credential_id>/', views.toggle_password, name='toggle_password'),
    path('api/copy-password/<int:credential_id>/', views.copy_password, name='copy_password'),
]
