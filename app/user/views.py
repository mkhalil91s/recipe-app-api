from django.shortcuts import render

# Create your views here.


### Views for the user API


from rest_framework import generics
from user.serializers import UserSerializer ## We defined


class CreateUserView(generics.CreateAPIView):
    
    """ Create a new user in the system."""  ## 
    
    serializer_class = UserSerializer