from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    HABIT_TYPE_CHOICES = [
        ('duration', 'Duration'),
        ('boolean', 'Boolean'),
        ('count', 'Count'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    type = models.CharField(max_length=20, choices=HABIT_TYPE_CHOICES)
    unit = models.CharField(max_length=50,blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    color = models.CharField(max_length=20, default='0xFF2196F3')
    icon = models.CharField(max_length=50, default='track_changes')

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    date = models.DateField()
    value = models.FloatField(default=0.0)
    completed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.habit.name} - {self.date}"