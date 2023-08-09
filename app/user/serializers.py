from django.contrib.auth import get_user_model


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