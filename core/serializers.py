from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Habit, HabitLog

# User Authentication Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account disabled')
            data['user'] = user
            return data
        raise serializers.ValidationError('Must include username and password')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined')

# Habit Serializers
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Habit.objects.create(**validated_data)


class HabitLogSerializer(serializers.ModelSerializer):
    habit_name = serializers.ReadOnlyField(source='habit.name')

    class Meta:
        model = HabitLog
        fields = '__all__'
        read_only_fields = ('habit',)

    def create(self, validated_data):
        habit = self.context.get('habit')
        validated_data['habit'] = habit
        return HabitLog.objects.create(**validated_data)
