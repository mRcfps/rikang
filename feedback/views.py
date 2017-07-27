from rest_framework import generics

from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackCreateView(generics.CreateAPIView):
    """Users `POST` their feedbacks through this endpoint."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
