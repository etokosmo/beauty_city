from django.urls import path

from .views import service_page, index_page

app_name = "service"

urlpatterns = [
    path('service/', service_page, name="service_page"),
    path('', index_page, name="index_page")
]
