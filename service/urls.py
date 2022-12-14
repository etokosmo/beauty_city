from django.urls import path
from . import views


urlpatterns = [
    path('service/', views.service_page, name="service_page"),
    path('', views.index_page, name="index_page")
]

