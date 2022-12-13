from django.urls import path
from . import views


urlpatterns = [
    path('', views.service_page, name="service_page")

]

