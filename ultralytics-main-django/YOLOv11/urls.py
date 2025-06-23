from django.contrib import admin
from django.urls import include, path

# Modular routing configuration
admin_routes = [path('admin/', admin.site.urls)]
home_routes = [path('', include('home.urls'))]
user_routes = [path('', include('user.urls'))]

# Summarize all routes
urlpatterns = admin_routes + home_routes + user_routes
