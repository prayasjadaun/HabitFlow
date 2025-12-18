from django.contrib import admin
from .models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'unit', 'is_active', 'created_at']
    list_filter = ['type', 'is_active']
    search_fields = ['name']

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'value', 'completed']
    list_filter = ['completed', 'date']
    search_fields = ['habit__name']