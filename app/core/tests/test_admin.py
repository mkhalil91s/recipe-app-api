""" 

Test from django admin modificaitons
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client



class AdminSiteTests(TestCase):
    """Tests for Django admin"""
    
    def setUp(self):
        """Create user and client."""
        
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'mina@gmail.com',
            password = '123456',
        )
        
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'testpass123',
            name = 'TestUser'
        ) 


    def test_users_list(self):
        """Test that users are listed on the page"""

        url = reverse('admin:core_user_changelist') ##We get the page that has the list of users
        res = self.client.get(url) ## Makes http get request , authenticated as admin user
        
        self.assertContains(res, self.user.name)  ##
        self.assertContains(res, self.user.email)