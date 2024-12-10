from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from .serializers import RegistrationSerializer, LoginSerializer,UserSerializer,UserProfileUpdateSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsOwner

# Registration View
class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate email confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/api/users/activate/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_template = 'confirm_teacher_email.html'  # Email template name

            # Render email body
            email_body = render_to_string(email_template, {'confirm_link': confirm_link})

            # Send email
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({"detail": "Check your email to activate your account."}, status=201)
        return Response(serializer.errors, status=400)


# Activation View
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:8000/api/users/login')
    else:
        return redirect('http://127.0.0.1:8000/api/users/register')


# Login View
class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        return Response(serializer.errors, status=400)


# Logout View
class UserLogoutAPIView(APIView):
    def post(self, request):
        try:
            token = request.auth  # Get the token sent with the request
            if token:
                token.delete()
            return Response({"detail": "Logged out successfully."}, status=200)
        except AttributeError:
            return Response({"detail": "No token provided."}, status=400)


# List all users
class UserListAPIView(APIView):
    """Retrieve a list of all users."""
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


# Retrieve details of a specific user
class UserDetailAPIView(APIView):
    """Retrieve details of an individual user."""
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)
        

class UserProfileUpdateAPIView(APIView):
    """
    Allows the authenticated user to update their own profile/account information.
    """
    permission_classes = [IsAuthenticated, IsOwner]  # Combine both permissions.

    def put(self, request):
        serializer = UserProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profile updated successfully.", "data": serializer.data}, status=200)
        
        return Response({"detail": "Invalid data", "errors": serializer.errors}, status=400)