from django.shortcuts import render

# Create your views here.


### Views for the user API


from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken ##We will use an exisiting view that is provided by the Django framework
from user.serializers import UserSerializer ## We defined
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system."""  ## 
    serializer_class = UserSerializer




class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
