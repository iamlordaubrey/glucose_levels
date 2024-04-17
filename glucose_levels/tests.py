from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from glucose_levels.models import GlucoseLevel, CustomUser


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

