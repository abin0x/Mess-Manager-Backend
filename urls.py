from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel URL
    path('api/', include('users.urls')),  # Routes for the 'users' app
    path('api/', include('mess.urls')),  
    path('api-auth/', include('rest_framework.urls')),
]
