from django.urls import path
from .views import *


app_name = 'students'

urlpatterns = [
    path('register_course/<slug:slug>',register_course, name="register_course"),       
]