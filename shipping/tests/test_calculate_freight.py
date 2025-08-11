from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from shipping.models import Country, Category

class CalculateFreightTest(TestCase):
    def setUp(self):
        # Buat data Country & Category
        self.country = Country.objects.create(
            country_name="Indonesia",
            origin_city_id=152,  # contoh ID Jakarta
        )
        self.category = Category.objects.create(
            country=self.country,
            category_title="Elektronik",
            price_per_kilo=100000  # harga internasional per kg
        )

        self.url = reverse('calculate_freight')

    @patch('shipping.views.requests.post')
    def test_calculate_with_mocked_rajaongkir(self, mock_post):
        # Mock respons RajaOngkir
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "meta": {"status": "success"},
            "data": [
                {"code": "jne", "cost": 60000},
                {"code": "pos", "cost": 80000}
            ]
        }

        payload = {
            "category_id": self.category.id,
            "destination_id": 501,  # contoh tujuan
            "weight": 2.5
        }

        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()

        # Cek hasil
        self.assertEqual(data['origin'], "Indonesia")
        self.assertEqual(data['category_name'], "Elektronik")
        self.assertEqual(data['international_price'], 250000)  # 2.5 * 100000
        self.assertEqual(data['domestic_price'], 60000)  # dari mock JNE
        self.assertEqual(data['total_price'], 310000)  # 250000 + 60000
