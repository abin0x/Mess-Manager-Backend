from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    confirm_password = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'user_type']

    def validate(self, data):
        """Validate password matching and email uniqueness."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"error": "Email is already registered"})

        return data

    def create(self, validated_data):
        """Handle user creation."""
        # Extract fields from the validated data
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user_type = validated_data['user_type']
        password = validated_data['password']

        # Create the user
        user = CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            is_active=False  # The user remains inactive until email confirmation
        )
        user.set_password(password)  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate the user login credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        
        if user is None:
            raise serializers.ValidationError({"error": "Invalid credentials"})
        
        if not user.is_active:
            raise serializers.ValidationError({"error": "Account is not active. Please confirm your email."})

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer to return user details."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type']



class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
