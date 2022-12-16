from django.urls import path

from .auth_tools import set_passcode, verify_user, logout_user
from .views import service_page, index_page, note_page, servicefinally_page

app_name = "service"

urlpatterns = [
    path('service/', service_page, name="service_page"),
    path('', index_page, name="index_page"),
    path('set_passcode/', set_passcode, name="set_passcode"),
    path('verify_user/', verify_user, name="verify_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('note/', note_page, name="note_page"),
    path('servicefinally/', servicefinally_page, name="servicefinally_page"),
]
