import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from property.models import Product


@pytest.mark.django_db
class TestProductSearchView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.product1 = Product.objects.create(
            name='product1',
            category='category1',
            brand='brand1',
            price=20,
            quantity=10,
            rating=4
        )
        self.product2 = Product.objects.create(
            name='product2',
            category='category2',
            brand='brand2',
            price=30,
            quantity=5,
            rating=3
        )
        self.product3 = Product.objects.create(
            name='product3',
            category='category1',
            brand='brand1',
            price=40,
            quantity=15,
            rating=5
        )
        self.product4 = Product.objects.create(
            name='product4',
            category='category2',
            brand='brand2',
            price=50,
            quantity=20,
            rating=2
        )
        self.url = reverse('product-search')
        self.user = self.setup_user()
        self.token = RefreshToken.for_user(self.user).access_token

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_search_by_category(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(self.url, {'category': 'category1'})

        # Ensure that the correct list of matching products is returned in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'product1'
        assert response.data[1]['name'] == 'product3'

    def test_search_by_brand(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(self.url, {'brand': 'brand1'})

        # Ensure that the correct list of matching products is returned in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'product1'
        assert response.data[1]['name'] == 'product3'

    def test_search_by_price_range(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        response = self.client.get(self.url, {'min_price': 20, 'max_price': 50})

        # Ensure that the correct list of matching products is returned in the response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'product1'
        assert response.data[1]['name'] == 'product3'
