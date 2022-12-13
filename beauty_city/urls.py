from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('service.urls')),
    path('', RedirectView.as_view(url='/service/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)