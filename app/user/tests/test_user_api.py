
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')  ## URL that we will add for creating tokens
#ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    
    return get_user_model().objects.create_user(**params)

##Public tests --> Unauthenticated requests (for example registering a new user)
##Private tests --> Required authentication


class PublicUserApiTests(TestCase):
    """ Test the public features of the user API"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test creating a user is successful."""
        
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        
        res = self.client.post(CREATE_USER_URL,payload) ## Call the URL and pass the payload
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        user = get_user_model().objects.get(email=payload['email'])
        
        self.assertTrue(user.check_password(payload['password'])) ## check the password exists
                        
        self.assertNotIn('password' , res.data)  ## Assert that the password is not part of the response returned by calling create user payload 
    
    def test_user_with_email_exists_error(self):
        
        payload = {
            'email' : 'test@example.com',
            'password': 'testpass123',
            'name' : 'Test  Name'
        }
        
        create_user(**payload) ## Passing the payload as email = , password = , name = 
        
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) ## If the email already exists , it will return an error
        
        
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        
        
        payload = {
            'email' : 'test@example.com',
            'password': 'pw',
            'name' : 'Test  Name'
        }
        
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists= get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        
        self.assertFalse(user_exists)

    
    def test_create_token_for_user(self):
        """Generate tokens for valid credentials"""
        
        user_details= {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-passsword123',
        }
        
        create_user(**user_details)
        
        
        payload = {
            'email' : user_details['email'],
            'password' : user_details['password'],
        }
        
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        
    def test_create_bad_credentials(self):
        """Test returns error if credentials invalid"""
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com' , 'passsword': 'badpassword'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        
        payload = {'email': 'test@example.com' , 'passsword': ''}
        
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    # def test_retrieve_user_unauthorized(self):
    #     """ Test authentication is required for users"""

    #     res = self.client.get(ME_URL)
    #      self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)