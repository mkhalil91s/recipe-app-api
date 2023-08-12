"""
Views for the recipe APIs 

"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


"""IF the user is calling the detail endpoint, the detail point api will be used"""

class RecipeViewSet(viewsets.ModelViewSet): ##Model view set directly set to work with a model
### View set will generate multiple different endpoints
    """View for manage recipe APIs"""

    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication] ##To use any of these views , you must use token authentication and you must be authenticated
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by('-id')


    def get_serializer_class(self): ## We are overriding 
        """Return the serializer class for request"""

        if self.action == 'retrieve':
            return serializers.RecipeSerializer ## Here you are returning a reference to the class and not an object to the class
        
        return self.serializer_class