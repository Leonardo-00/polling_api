from rest_framework.response import Response

from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from useraccounts.models import Account
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model

from useraccounts.serializers import CustomUpdateSerializer

from polls.models import Poll, Category
from polls.serializers import PollSerializer

User = get_user_model()

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Restituisce sempre l’utente attualmente autenticato
        return self.request.user

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({"username": f"{request.user.username}"})

# A view to manage user interests
# This view allows users to retrieve and update their interests (favorite categories)
class UserInterestViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
        except Account.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        polls = Poll.objects.exclude(created_by=user).filter(category__in=user.favorite_categories.all())
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
