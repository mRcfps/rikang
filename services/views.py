from rest_framework import generics

from services.serializers import ConsultationSerializer


class CreateConsultationView(generics.CreateAPIView):

    serializer_class = ConsultationSerializer
