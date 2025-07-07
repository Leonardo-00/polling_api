from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from polls.models import Category


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    favorite_categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'favorite_categories': self.validated_data.get('favorite_categories', [])
        }
        
    def save(self, request):
        user = super().save(request)
        cleaned_data = self.get_cleaned_data()
        categories = cleaned_data.get('favorite_categories', [])
        if categories:
            # assegna le categorie many-to-many
            user.favorite_categories.set(categories)
        user.save()
        return user