from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

from rest_framework import viewsets
from .models import Poll
from .serializers import PollSerializer
from .permissions import IsOwnerOrReadOnly

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        # Associa automaticamente l'utente autenticato come creatore del sondaggio
        serializer.save(created_by=self.request.user)
        



class LoggedInUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": f"Benvenuto, {request.user.username}!"})
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()  # Assuming you want to list all polls for the category
    serializer_class = PollSerializer  # Use the appropriate serializer for categories
    permission_classes = [IsOwnerOrReadOnly]  # Adjust permissions as needed

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Poll.objects.filter(category__name=category_name)  # Filter by category name