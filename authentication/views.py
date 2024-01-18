from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserRegSerializer, GoogleSocialAuthSerializer

# Create your views here.
class Register(APIView):        
    def post(self, request, format=None, *args, **kwargs):
        # hash password before serializing
        request.data['password'] = make_password(request.data['password'])

        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('User created')
            
            user = User.objects.get(username=serializer.data['username'])
            print(user)
            user_token = Token.objects.get(user=user).key
            response = {
                'username': serializer.data['username'],
                'email': serializer.data['email'],
                'token': user_token
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GoogleSocialAuthView(APIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        if data["message"] == "user account created successfully":
            user = User.objects.get(id=data["user_id"])
            # Util.send_activation_otp(user)
            '''
            you can decide to handle how you want the OTP is going to be sent
            '''
            return Response({"message": "otp sent"}, status=status.HTTP_201_CREATED)

        elif data["message"] == "login successful":
            user = User.objects.get(id=data["user_id"])
            # Util.send_login_otp(user)
            '''
            you can decide to handle how you want the OTP is going to be sent
            or you can decide to just generate the access tokens and return 
            it as response
            '''
            return Response({"message": "login successful"}, status=200)

        elif data["message"] == "account not activated":
            return Response(
                {"message": "account not activated", "user_id": data["user_id"], "email": data["email"]}, status=400)

register = Register.as_view()