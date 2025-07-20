from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('auth/', include('authentication.urls')),
    path('', include('authentication.template_urls')),  # This handles /, /login/, /register/, etc.
]
