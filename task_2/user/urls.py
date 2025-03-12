from django.urls import path
from user.views import User

urlpatterns = [
    path("", User.as_view(), name="retrieve_user")
]