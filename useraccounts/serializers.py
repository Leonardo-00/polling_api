from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from polls.models import Category
from useraccounts.models import Account


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

class CustomUpdateSerializer(serializers.ModelSerializer):
    favorite_categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    
    oldpw = serializers.CharField(write_only=True, required=False, allow_blank=True)
    pw1 = serializers.CharField(write_only=True, required=False, allow_blank=True)
    pw2 = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'oldpw', 'pw1', 'pw2', 'first_name', 'last_name', 'favorite_categories']
        read_only_fields = ['id', 'username']
        
    def validate(self, attrs):
        super().validate(attrs)
        
        user = self.instance
        if 'oldpw' in attrs and 'pw1' in attrs:
            old_password = attrs['oldpw']
            password1 = attrs['pw1']
            if not user.check_password(old_password):
                raise serializers.ValidationError("Old password is incorrect.")
            if password1 != attrs.get('pw2'):
                raise serializers.ValidationError("New passwords do not match.")
            if len(password1) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long.")

        if 'favorite_categories' in attrs:
            categories = attrs['favorite_categories']
            if not isinstance(categories, list):
                raise serializers.ValidationError("Favorite categories must be a list of category IDs.")
            for category in categories:
                if not Category.objects.filter(name=category.name).exists():
                    raise serializers.ValidationError(f"Category with name {category.name} does not exist.")
                
            if len(categories) < 1:
                raise serializers.ValidationError("You must select at least one favorite category.")
            
            if len(categories) > 3:
                raise serializers.ValidationError("You can select a maximum of 3 favorite categories.")
        return attrs
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        categories = validated_data.get('favorite_categories', [])
        if categories:
            instance.favorite_categories.set(categories)
        
        if 'pw1' in validated_data:
            instance.set_password(validated_data['pw1'])
        
        instance.save()
        return instance
