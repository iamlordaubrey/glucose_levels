from rest_framework import generics

from glucose_levels.models import GlucoseLevel
from glucose_levels.serializers import GlucoseLevelSerializer


class GlucoseLevelList(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer
    queryset = GlucoseLevel.objects.all()
