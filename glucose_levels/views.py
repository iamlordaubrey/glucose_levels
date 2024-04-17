from rest_framework import generics

from glucose_levels.models import GlucoseLevel
from glucose_levels.pagination import GlucoseLevelPagination
from glucose_levels.serializers import GlucoseLevelSerializer


class GlucoseLevelList(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer
    queryset = GlucoseLevel.objects.all()
    pagination_class = GlucoseLevelPagination

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        start_timestamp = self.request.query_params.get('start')
        stop_timestamp = self.request.query_params.get('stop')

        queryset = GlucoseLevel.objects.filter()
        if user_id:
            queryset = queryset.filter(user=user_id)
        if start_timestamp:
            queryset = queryset.filter(timestamp__gte=start_timestamp)
        if stop_timestamp:
            queryset = queryset.filter(timestamp__lte=stop_timestamp)
        return queryset


class GlucoseLevelDetail(generics.RetrieveAPIView):
    serializer_class = GlucoseLevelSerializer
    queryset = GlucoseLevel.objects.all()

