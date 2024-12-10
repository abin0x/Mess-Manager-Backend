from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='member')


    def is_manager(self):
        """Check if the user is a manager"""
        return self.user_type == 'manager'

    def __str__(self):
        return self.username
