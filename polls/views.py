from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from useraccounts.models import Account

from .models import Category, Poll
from .serializers import *

# permissions
from rest_framework.permissions import AllowAny
from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly

import django_filters
from django.core.exceptions import PermissionDenied

class PollFilter(django_filters.FilterSet):
    interest = django_filters.CharFilter(method='filter_by_interest')
    username = django_filters.CharFilter(field_name='created_by__username', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    def filter_by_interest(self, queryset, name, value):
        interest = self.request.query_params.get('interest')
        if interest == "true":
            user = self.request.user
            if not user.is_authenticated:
                raise PermissionDenied("Authentication required to view your interests.")
            
            categories = user.favorite_categories.all()
            return queryset.filter(category__in=categories).exclude(created_by=user)
        return queryset

    class Meta:
        model = Poll
        fields = ['category__name', 'created_by__username']

# ViewSet for creation and retrieval of polls
class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Poll.objects.all().order_by('-created_at')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__name', 'created_by__username']
    filterset_class = PollFilter
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

#A view to list all categories
class CategoriesListView(APIView):
    
    serializer = CategorySerializer
    
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

#A view to handle voting on polls
# This view allows users to vote on a poll and retrieves votes for a specific poll
class VoteViewSet(APIView):
    VoteSerializer = VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=404)

        votes = poll.vote_set.all()
        serializer = self.VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        option_id = request.data.get('option_id')
        
        if not option_id:
            return Response({"error": "Option ID is required"}, status=400)
        
        if request.user == poll.created_by:
            return Response({"error": "You cannot vote on your own poll"}, status=403)
        
        try:
            choice = poll.choices.get(id=option_id)
        except Choice.DoesNotExist:
            return Response({"error": "Option not found"}, status=404)
        

        vote, created = Vote.objects.update_or_create(
            poll=poll,
            voted_by=request.user,
            defaults={'choice': choice}
        )

        if created:
            return Response({"message": "Vote registered."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Vote updated."}, status=status.HTTP_200_OK)

# A view to retrieve poll results
# This view retrieves the results of a specific poll, including the number of votes for each choice
@api_view(['GET'])
@permission_classes([AllowAny])
def get_poll_results(request, poll_id):
    
    poll = get_object_or_404(Poll, id=poll_id)
    choices = (
        poll.choices
        .annotate(votes_count=models.Count("votes"))
        .values("id", "text", "votes_count")
    )

    results = []
    for choice in choices:
        result = {}
        
        result["id"] = choice["id"]
        result["text"] = choice["text"]
        result["votes"] = choice["votes_count"]
        if(request.user.is_authenticated):
            if(Vote.objects.filter(poll=poll, choice__text=choice["text"], voted_by=request.user).exists()):
                result["voted"] = True
            else:
                result["voted"] = False
        results.append(result)

    data = {
        "poll_id": poll.id,
        "question": poll.question,
        "choices": results
    }

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_polls(request):
    if request.user.is_authenticated:
        polls = Poll.objects.filter(created_by=request.user).order_by('-created_at')
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)