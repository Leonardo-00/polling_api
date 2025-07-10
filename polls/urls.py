from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', PollViewSet, basename='poll')



urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='category'),
    path('vote/<int:poll_id>/', VoteViewSet.as_view(), name='vote'),
    path('<int:poll_id>/results/', PollResultsView.as_view(), name='poll-results'),
    path('', include(router.urls)),
]