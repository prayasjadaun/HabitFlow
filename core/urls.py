from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    habit_list_create, habit_detail, habit_logs,
    register, login, profile, logout
)

urlpatterns = [
    # Authentication URLs
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', profile, name='profile'),
    
    # Habit URLs
    path('habits/', habit_list_create),
    path('habits/<int:pk>/', habit_detail),
    path('habits/<int:habit_id>/logs/', habit_logs),
]