from django.urls import path
from .views import register_view, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', register_view, name='signup'),  # Use only 'signup' to match your UI
]
