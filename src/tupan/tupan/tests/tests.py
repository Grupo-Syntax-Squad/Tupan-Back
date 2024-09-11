import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_homepage(client):
    url = reverse('admin')
    response = client.get(url)
    assert response.status_code == 200
