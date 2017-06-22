from rest_framework import generics

from home.models import Post, Hospital
from home.serializers import (PostListSerializer,
                              PostDetailSerializer,
                              HospitalListSerializer,
                              HospitalDetailSerializer)


class PostListView(generics.ListAPIView):
    """GET a collection of posts."""

    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailView(generics.RetrieveAPIView):
    """GET a single post by id."""

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class HospitalListView(generics.ListAPIView):
    """GET a collection of hospitals."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalListSerializer


class HospitalDetailView(generics.RetrieveAPIView):
    """GET a single hospital by id."""

    queryset = Hospital.objects.all()
    serializer_class = HospitalDetailSerializer
