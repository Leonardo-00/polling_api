
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', obtain_auth_token),
    path('api/polls/', include('polls.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),  # login/logout/password reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/users/', include('useraccounts.urls')),
]
