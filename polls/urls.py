from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoriesListView.as_view(), name='category'),
    path('interest/', InterestCategoryViewSet.as_view(), name='interest-category'),
    path('interest/<int:user_id>/', UserInterestViewSet.as_view(), name='interest-category-user'),
    path('vote/<int:poll_id>/', VoteViewSet.as_view(), name='vote'),
]