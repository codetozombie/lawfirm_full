# Create your models here.
from django.db import models

class Attorney(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='attorneys/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry from {self.name}"