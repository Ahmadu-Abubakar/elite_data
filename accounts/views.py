from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework.views import APIView
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from .services import (
    send_verification_email,
    login_user,
    )
from . services import (
    InvalidCredentialsError,
    EmailNotVerifiedError
)
from .token_service import (
    generate_email_verification_token,
    verify_email_verification_token,
    refresh_access_token,
    InvalidTokenError
)
from rest_framework.views import APIView




class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        token = generate_email_verification_token(
            user
        )

        send_verification_email(
            user,
            token
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        ) 

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email_view(request, token):


    try:
        verify_email_verification_token(token)

        return Response(
            {
                "message" : "Email verified successfully!"
            },
            status=status.HTTP_200_OK
        )
    
    
    except Exception as e:
        return Response(
            {
                "error" : str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        ) 
    
    


# login view___________
class LoginView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):


        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )


        try:
            token_data = login_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
        
        except InvalidCredentialsError as e:
            return Response ({
                "message" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except EmailNotVerifiedError as e:
            return Response ({
                "message" : str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        

        return Response (
            token_data, 
            status=status.HTTP_200_OK
        )
    


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)

        serializer.is_valid(
            raise_exception=True
        )

        token = serializer.validated_data["refresh_token"]
         
        try:
            token_data = refresh_access_token(token)
        except InvalidTokenError as e:
            return Response({
                "message" : str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(
            token_data,
            status=status.HTTP_200_OK
        )

        
# Create your views here.

