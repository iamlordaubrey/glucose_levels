from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from glucose_levels.models import GlucoseLevel
from glucose_levels.pagination import GlucoseLevelPagination
from glucose_levels.serializers import GlucoseLevelSerializer, GlucoseLevelCreateSerializer


class GlucoseLevelList(generics.ListAPIView):
    serializer_class = GlucoseLevelSerializer
    queryset = GlucoseLevel.objects.all()
    pagination_class = GlucoseLevelPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ('-timestamp',)

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


class GlucoseLevelCreate(generics.CreateAPIView):
    serializer_class = GlucoseLevelCreateSerializer

    def create(self, request, *args, **kwargs):
        print('create', request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
