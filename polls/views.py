from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework import viewsets

from useraccounts.models import Account
from .models import Category, Poll
from .serializers import *

# permissions
from rest_framework.permissions import AllowAny
from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly


# ViewSet for creation and retrieval of polls
class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
    def get_queryset(self):    
        queryset = Poll.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

#A viewset to retrieve polls by category
# This assumes that you have a foreign key relationship from Poll to Category 
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('-created_at')
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Poll.objects.filter(category__name=category_name)

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
            return Response({"message": "Voto registrato."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Voto aggiornato."}, status=status.HTTP_200_OK)

# A view to retrieve poll results
# This view retrieves the results of a specific poll, including the number of votes for each choice
class PollResultsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        choices = (
            poll.choices
            .annotate(votes_count=models.Count("votes"))
            .values("id", "text", "votes_count")
        )

        results = []
        for choice in choices:
            if(request.user.is_authenticated and Vote.objects.filter(poll=poll, choice__text=choice["text"], voted_by=request.user).exists()):
                voted = True
            else:
                voted = False
            results.append({
                "id": choice["id"],
                "text": choice["text"],
                "votes": choice["votes_count"],
                "voted": voted
            })

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
        polls = Poll.objects.filter(created_by=request.user)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)