from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

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
        # Associa automaticamente l'utente autenticato come creatore del sondaggio
        serializer.save(created_by=self.request.user)
        
    def get_queryset(self):    
        queryset = Poll.objects.all()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


#A viewset to retrieve polls by category
# This assumes that you have a foreign key relationship from Poll to Category 
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()  # Assuming you want to list all polls for the category
    serializer_class = PollSerializer  # Use the appropriate serializer for categories
    permission_classes = [IsOwnerOrReadOnly]  # Adjust permissions as needed

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Poll.objects.filter(category__name=category_name)  # Filter by category 


#A view to get all the polls of interest for a user
# This view retrieves polls that belong to the user's favorite categories, excluding polls created by the user
class InterestCategoryViewSet(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        interests = user.favorite_categories.all()
        polls =  Poll.objects.filter(category__in=interests).exclude(created_by=user)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    
    def updateUserInterests(self, request, user_id):
        user = Account.objects.get(id=user_id)
        interests = request.data.get('interests', [])
        
        # Clear existing interests
        user.favorite_categories.clear()
        
        # Add new interests
        for interest in interests:
            category = Category.objects.get(name=interest)
            user.favorite_categories.add(category)
        
        return Response({"message": "User interests updated successfully"})




#A view to list all categories
class CategoriesListView(APIView):
    
    serializer = CategorySerializer
    
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class VoteViewSet(APIView):
    VoteSerializer = VoteSerializer  # Assuming you have a serializer for votes
    permission_classes = [IsAuthenticatedOrReadOnly]  # Custom permission to check if the user can vote
    
    def get(self, request, poll_id):
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"error": "Poll not found"}, status=404)

        # Retrieve all votes for the poll
        votes = poll.vote_set.all()
        serializer = self.VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        option_id = request.data.get('option_id')
        
        if not option_id:
            return Response({"error": "Option ID is required"}, status=400)

        try:
            option = poll.choices.get(id=option_id)
        except Choice.DoesNotExist:
            return Response({"error": "Option not found"}, status=404)

        # Add the vote
        vote = self.VoteSerializer(data={
            'poll': poll.id,
            'choice': option.id,
            'voted_by': request.user.id
        })
        if not vote.is_valid():
            return Response(vote.errors, status=400)
        vote.save()

        return Response({"message": "Vote recorded successfully"})