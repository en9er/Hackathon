from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL
urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

