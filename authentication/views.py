from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserRegSerializer

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

register = Register.as_view()