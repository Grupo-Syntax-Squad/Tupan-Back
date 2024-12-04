import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_create_user():
    client = APIClient()
    url = "http://localhost:8000/usuarios/"
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['email'] == "test@example.com"