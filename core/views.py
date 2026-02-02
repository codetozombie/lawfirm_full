from rest_framework import viewsets, mixins, permissions
from django.core.mail import send_mail
from django.conf import settings
from .models import Attorney, ContactSubmission
from .serializers import AttorneySerializer, ContactSubmissionSerializer
import os

class AttorneyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attorney.objects.filter(is_active=True)
    serializer_class = AttorneySerializer
    permission_classes = [permissions.AllowAny]

class ContactSubmissionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # 1. Save to Database first
        submission = serializer.save()

        # 2. Send Email Notification
        subject = f"New Legal Inquiry from {submission.name}"
        message = f"""
        You have received a new inquiry on the website.

        Name: {submission.name}
        Email: {submission.email}
        Phone: {submission.phone}
        
        Message:
        {submission.message}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL, # Sender
                [os.environ.get('RECIPIENT_EMAIL')], # Recipient (You)
                fail_silently=False,
            )
        except Exception as e:
            # Print error to console but don't crash the user's request
            print(f"Email failed to send: {e}")