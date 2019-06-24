from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
	path('calculate_sgpa', views.calculate_sgpa, name='calculate_sgpa')
]
