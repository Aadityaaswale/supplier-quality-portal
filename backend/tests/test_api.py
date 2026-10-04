import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_check_endpoint():
    client = APIClient()
    response = client.get('/health/')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert data['database'] == 'ok'
    assert 'student' in data


@pytest.mark.django_db
def test_dashboard_summary_api():
    client = APIClient()
    user = User.objects.create_user(username='api_user', password='Password123')
    client.force_authenticate(user=user)

    response = client.get('/api/dashboard/summary/')
    assert response.status_code == 200
    data = response.json()
    assert 'kpis' in data
    assert 'charts' in data
    assert 'total_suppliers' in data['kpis']
