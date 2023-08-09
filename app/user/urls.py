"""

URL mappings for the user API

"""


from django.urls import path
from user import views


app_name = 'user'  ## It will be used for the reverse mapping in the test_user_api


urlpatterns = [
    path('create/' , views.CreateUserView.as_view(), name = 'create'),
]

