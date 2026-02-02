from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttorneyViewSet, ContactSubmissionViewSet

router = DefaultRouter()
router.register(r'attorneys', AttorneyViewSet, basename='attorney')
router.register(r'contact', ContactSubmissionViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
]
