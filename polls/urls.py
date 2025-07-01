from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'categories', CategoryViewSet, basename='category')  # Assuming you want to use the same viewset for categories
router.register(r'interests', InterestCategoryViewSet, basename='interest-category')

urlpatterns = [
    path('', include(router.urls)),
]