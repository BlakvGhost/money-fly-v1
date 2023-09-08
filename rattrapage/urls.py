from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('banque.urls')),
    path('auth/', include('authentification.urls')),
]
