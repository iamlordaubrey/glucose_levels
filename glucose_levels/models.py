import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    id = models.CharField(max_length=200, primary_key=True, unique=True)

    USERNAME_FIELD = 'id'


User = get_user_model()


class GlucoseLevel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    device = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200)
    timestamp = models.DateTimeField()
    recording_type = models.IntegerField(default=0)
    glucose_value_history = models.IntegerField(blank=True, null=True)
    glucose_scan = models.IntegerField(blank=True, null=True)
    non_numeric_rapid_acting_insulin = models.CharField(max_length=200, blank=True, null=True)
    rapid_acting_insulin = models.IntegerField(blank=True, null=True)
    non_numeric_nutritional_data = models.CharField(max_length=200, blank=True, null=True)
    carbohydrates_grams = models.IntegerField(blank=True, null=True)
    carbohydrates_portion = models.IntegerField(blank=True, null=True)
    non_numeric_depot_insulin = models.CharField(max_length=200, blank=True, null=True)
    depot_insulin = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    glucose_test_strip = models.IntegerField(blank=True, null=True)
    ketone = models.IntegerField(blank=True, null=True)
    meal_insulin = models.IntegerField(blank=True, null=True)
    correction_insulin = models.IntegerField(blank=True, null=True)
    insulin_change_by_user = models.IntegerField(blank=True, null=True)