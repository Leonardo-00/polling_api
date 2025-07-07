from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class LoggedInUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": f"{request.user.username}"})