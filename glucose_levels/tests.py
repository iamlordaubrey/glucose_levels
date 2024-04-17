from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from glucose_levels.models import GlucoseLevel, CustomUser
from glucose_levels.serializers import CustomUserSerializer


class GlucoseLevelsRetrieveAndPaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_id = 'aaa'
        self.custom_user = CustomUser.objects.create(id=self.user_id)
        self.glucose_level = GlucoseLevel.objects.create(
            user=self.custom_user,
            device='A device',
            serial_number='123456',
            timestamp='2024-04-17T12:00:00Z'
        )

    def test_retrieve_glucose_level(self):
        url = reverse('glucose_level_list')
        response = self.client.get(url, {'user_id': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_glucose_level_by_id(self):
        url = reverse('glucose_level_detail', args=[self.glucose_level.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.glucose_level.id))

    def test_pagination(self):
        url = reverse('glucose_level_list')
        response = self.client.get(url, {'user_id': self.user_id, 'page': 1, 'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class GlucoseLevelsSortingAndFilteringTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_id = 'bbb'
        self.custom_user = CustomUser.objects.create(id=self.user_id)
        self.glucose_level = [
            GlucoseLevel.objects.create(
                user=self.custom_user,
                device='A device',
                serial_number='123',
                timestamp='2024-04-17T12:00:00Z'
            ),
            GlucoseLevel.objects.create(
                user=self.custom_user,
                device='A device',
                serial_number='234',
                timestamp='2024-04-18T12:00:00Z'
            ),
            GlucoseLevel.objects.create(
                user=self.custom_user,
                device='A device',
                serial_number='345',
                timestamp='2024-04-16T12:00:00Z'
            ),
        ]

    def test_sorting(self):
        url = reverse('glucose_level_list')
        response = self.client.get(url, {'user_id': self.user_id, 'ordering': 'timestamp'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

        # Sorted by timestamp. The first is GlucoseLevel object at index 2
        self.assertEqual(response.data['results'][0]['serial_number'], self.glucose_level[2].serial_number)

        # The third is GlucoseLevel object at index 1
        self.assertEqual(response.data['results'][2]['serial_number'], self.glucose_level[1].serial_number)

    def test_timestamp_filtering(self):
        url = reverse('glucose_level_list')
        response = self.client.get(url, {'user_id': self.user_id, 'start': '2024-04-16T12:00', 'stop': '2024-04-16T22:00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['serial_number'], self.glucose_level[2].serial_number)
