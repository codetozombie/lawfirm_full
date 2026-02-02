from rest_framework import serializers
from .models import Attorney, ContactSubmission

class AttorneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = ['id', 'name', 'role', 'specialty', 'bio', 'image', 'is_active']

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['id', 'name', 'email', 'phone', 'message', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']