from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ("Admin", "Admin"),
    ("Manager", "Manager"),
    ("Employee", "Employee"),
)

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Employee")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
