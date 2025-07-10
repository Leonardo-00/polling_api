from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()


urlpatterns = [
    path('whoami/', whoami, name='whoami'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
