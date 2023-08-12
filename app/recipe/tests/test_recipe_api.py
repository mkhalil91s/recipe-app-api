### Test for recipe APIs.


from decimal import Decimal


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import (RecipeSerializer, RecipeDetailSerializer) ## One serializer for perview and another one that adds more fields and give 
                                                                        ##more details for a specific recipe


RECIPES_URL = reverse('recipe:recipe-list')
##Helper func for creating a recipe 

def detail_url(recipe_id):
    """Create and return recipe url"""
    return reverse('recipe:recipe-detail', args = [recipe_id])

def create_recipe(user,**params):
    """Create and return a sample recipe."""

    defaults = {
        'title': 'Sample',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'www.recipe.com',
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call api"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )

        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Retrieve a list of recipe"""

    def test_retrive_recipes(self):
        """Test retrieving a list of recipes"""

        create_recipe(user = self.user)
        create_recipe(user = self.user)

        ###We will have 2 recipes created in Db

        res = self.client.get(RECIPES_URL) ## We should see 2 recipes returned here

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True) ## We expect the result to match what the serializer returns
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        recipe1 = create_recipe(user=other_user)
        recipe2 = create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        self.assertEqual(len(res.data), 1)
        self.assertNotIn(recipe1, res.data)

    def test_get_recipe_detail(self):
        """TEST GET RECIPE DETAIL"""

        recipe = create_recipe(user=self.user)
        url   = detail_url(recipe.id)
        res  = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)





    