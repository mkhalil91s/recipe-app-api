""" 

Tests for models.

"""

from django.test import TestCase ##So it doesn't create test case setups
from django.contrib.auth import get_user_model  ## To read the user model


class ModelTests(TestCase):
    
    
    def test_create_user_with_email_successful(self):
        
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
    
    
    def test_new_user_email_normalized (self):
        """Test email is normalized for new users"""
        
        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            [ 'Test2@Example.com' , 'Test2@example.com'],
            [ 'TEST3@EXAMPLE.COM' , 'TEST3@example.com'],
            [  'test4@example.com' , 'test4@example.com']
        ]
        
        for email,expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email, expected)
        
        
        
        
    def test_new_user_without_email_raises_error (self):
        """Users without an email raises a value error"""
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')
            

    def test_create_superuser (self):
        """Test creating a SuperUser"""
        
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)