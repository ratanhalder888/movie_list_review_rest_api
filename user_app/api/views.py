from rest_framework.decorators import api_view
from rest_framework.views import APIView
from user_app.api.serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email

            # TOKEN AUTHENTICATION
            # token = Token.objects.get(user=account).key
            # data['token'] = token

            # JWT AUTHENTICATION
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)
    

class RegistrationView(APIView):

     def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email

            # JWT AUTHENTICATION
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)
     

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        # JWT logout is typically handled on the frontend by deleting the token.
        # If blacklisting is enabled, you can blacklist the refresh token here.
        return Response({"message": "Logout successful (Client-side token removal recommended)"}, status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    """
    An API View to log out a user by deleting their authentication token.
    Requires the user to be authenticated to access this view.
    """
    # Ensures only authenticated users can hit this endpoint
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        """
        Handles the logout action.
        """
        try:
            # JWT is stateless; logout is handled by the client.
            # If blacklisting is used, the refresh token should be blacklisted.
            return Response(
                {"message": "Successfully logged out (Client-side token removal recommended)."}, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            # Handle cases where the token might already be deleted or missing
            return Response(
                {"error": "Failed to log out or token not found."}, 
                status=status.HTTP_400_BAD_REQUEST
            )