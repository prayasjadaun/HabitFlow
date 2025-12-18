from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Habit, HabitLog
from .serializers import (
    HabitSerializer, HabitLogSerializer, UserRegistrationSerializer, 
    UserLoginSerializer, UserProfileSerializer
)

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(UserProfileSerializer(request.user).data)

# Habit Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def habit_list_create(request):
    if request.method == 'GET':
        habits = Habit.objects.filter(user=request.user, is_active=True).order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 20  

        paginated_habits = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(paginated_habits, many=True)

        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        serializer = HabitSerializer(
            data=request.data,
            context={'request': request}   
        )
        if serializer.is_valid():
            serializer.save()              
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Habit Detail View
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def habit_detail(request, pk):
    try:
        habit = Habit.objects.get(pk=pk, user=request.user)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=404)

    if request.method == 'GET':
        return Response(HabitSerializer(habit).data)

    if request.method == 'PUT':
        serializer = HabitSerializer(
        habit,
        data=request.data,
        context={'request': request}
)
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        habit.delete()
        return Response(status=204)

# Habit Logs Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def habit_logs(request, habit_id):
    try:
        habit = Habit.objects.get(pk=habit_id, user=request.user)
    except Habit.DoesNotExist:
        return Response({'error': 'Habit not found'}, status=404)

    if request.method == 'GET':
        logs = HabitLog.objects.filter(habit=habit).order_by('-date')
        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_logs = paginator.paginate_queryset(logs, request)
        serializer = HabitLogSerializer(paginated_logs, many=True)
        return paginator.get_paginated_response(serializer.data)


    if request.method == 'POST':
        serializer = HabitLogSerializer(
        data=request.data,
        context={'request': request, 'habit': habit}
)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Logout View

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"})
    except Exception:
        return Response({"error": "Invalid token"}, status=400)