from django.db import models
from users.models import CustomUser  # Importing the CustomUser model
from django.utils import timezone

class Mess(models.Model):
    """Model to represent a Mess."""
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(default="N/A")
    manager = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name="managed_messes"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    


class MembershipRequest(models.Model):
    """
    Represents a membership request sent by a user to a specific mess.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="membership_requests")
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE, related_name="membership_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.mess.name} ({self.status})"
