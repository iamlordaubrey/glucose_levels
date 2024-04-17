from rest_framework import serializers

from glucose_levels.models import GlucoseLevel


class GlucoseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseLevel
        fields = '__all__'
