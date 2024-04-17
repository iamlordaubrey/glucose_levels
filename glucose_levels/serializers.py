from django.contrib.auth import get_user_model
from rest_framework import serializers

from glucose_levels.models import GlucoseLevel


class GlucoseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseLevel
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'


class GlucoseLevelCreateSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=True)

    class Meta:
        model = GlucoseLevel
        fields = '__all__'

    def create(self, validated_data):
        print('got here???')
        user_data = validated_data.pop('user')
        user_instance = get_user_model().objects.get_or_create(**user_data)[0]
        glucose_level = GlucoseLevel.objects.create(user=user_instance, **validated_data)
        return glucose_level
