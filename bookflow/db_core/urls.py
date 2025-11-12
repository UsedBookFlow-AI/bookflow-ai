from django.urls import path
from db_core.views import register_user_view

urlpatterns = [
    path('register/', register_user_view, name='register_user'),
]