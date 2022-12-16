from django.urls import path

from .auth_tools import set_passcode, verify_user, logout_user
from .views import service_page, index_page, note_page, servicefinally_page, \
    get_masters, get_services, get_categories, get_salons, profile_page

app_name = "service"

urlpatterns = [
    path('service/', service_page, name="service_page"),
    path('', index_page, name="index_page"),
    path('set_passcode/', set_passcode, name="set_passcode"),
    path('verify_user/', verify_user, name="verify_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('note/', note_page, name="note_page"),
    path('servicefinally/', servicefinally_page, name="servicefinally_page"),
    path('choose_salons/', get_salons, name="choose_salons"),
    path('choose_categories/', get_categories, name="choose_categories"),
    path('choose_services/', get_services, name="choose_services"),
    path('choose_masters/', get_masters, name="choose_masters"),
    path('profile/', profile_page, name="profile_page"),
]
