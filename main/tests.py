from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Cinema
from decimal import Decimal

# Create your tests here.
class RateCinemaAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cinema = Cinema.objects.create(
            name="Test Cinema",
            discription="A test cinema",
            cite_url="http://example.com",
            star=Decimal('0.0'),
            like_cnt=0,
            location="서울",
            latitude=37.579472,
            longitude=126.976872,
            rating_sum=Decimal('0.0'),
            rating_cnt=0
        )
        self.url = reverse('rating_cinema', kwargs={'pk': self.cinema.id})

    def test_rate_cinema(self):
        # 새로운 별점 4.2를 보내서 별점 업데이트
        response = self.client.post(self.url, {'rating': 4.2}, format='json')
        self.cinema.refresh_from_db()  # 데이터베이스에서 최신 데이터 가져오기

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cinema.rating_sum, Decimal('4.2'))
        self.assertEqual(self.cinema.rating_cnt, 1)
        self.assertEqual(self.cinema.star, Decimal('4.2'))