from django.contrib.auth import (
    get_user_model,
    authenticate, ## Function that comes with django that allows you to authenticate with the authentication syste,
)

from django.utils.translation import gettext as _


from rest_framework import serializers  ##Rest framework has serializers , serializers are a way to convert an object , to and from a python object



class UserSerializer(serializers.ModelSerializer): 

    """ Serializer for the user object."""
    
    class Meta:
    
        model=get_user_model()
        fields = ['email' , 'password' , 'name'] ## Fields avaialble for the serializer
        extra_kwargs = { 'password' : { 'write_only' : True , 'min_length' : 5}}
        
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        
        return get_user_model().objects.create_user(**validated_data)
    


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token"""
    
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'passsword'},
        trim_whitespace=False,
    )
    
    ##Validate message is called at the serializer on a validation stage
    

    def validate(self,attrs):
        """Validate and authenticate the user"""
        #When the data is posted to the view, it is gonna pass it to the serialize then it will validate it when the data is correct"
        
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate (   ### This function comes build in with Django
            request = self.context.get('request'),
            username = email,
            password = password,
        )
        
        if not user:
            msg = _("Unable to authenticate with provided credentials>")
            raise serializers.ValidationError(msg, code = 'authorization')
        
        attrs['user'] = user
        return attrs
        
        
    
    
    
    