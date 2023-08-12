"""
Serializers for recipe APIs

"""

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = ['id','title' , 'time_minutes' , 'price' , 'link']
        read_only_fields = ['id'] ## Si we cant change the id

class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail recipe"""

    class Meta(RecipeSerializer.Meta): ## Inheriting all details from the upper serializer and getting all the data
        fields = RecipeSerializer.Meta.fields + ['description']
        