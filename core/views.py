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
        # 1. Save the submission to the database
        submission = serializer.save()

        # ---------------------------------------------------------
        # Email 1: Notification to YOU (The Firm)
        # ---------------------------------------------------------
        admin_subject = f"New Legal Inquiry from {submission.name}"
        admin_message = f"""
        New website inquiry received:

        Name: {submission.name}
        Email: {submission.email}
        Phone: {submission.phone}
        
        Message:
        {submission.message}
        """
        
        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [os.environ.get('RECIPIENT_EMAIL')], # Sends to you
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")

        # ---------------------------------------------------------
        # Email 2: Confirmation to the CLIENT (The Sender)
        # ---------------------------------------------------------
        client_subject = "Inquiry Received - Amoako & Associates"
        client_message = f"""
        Dear {submission.name},

        Thank you for contacting Amoako & Associates. 

        We have received your inquiry and our team will review your message shortly. If your matter requires urgent attention, please call our office directly.

        Best Regards,
        
        Amoako & Associates
        Attorneys at Law
        """

        try:
            send_mail(
                client_subject,
                client_message,
                settings.DEFAULT_FROM_EMAIL, # Sent FROM your firm
                [submission.email],          # Sent TO the client
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send client confirmation: {e}")