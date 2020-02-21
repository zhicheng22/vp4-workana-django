from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.customer_register, name='customer_register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate_account, name='activate'),
]

