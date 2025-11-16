"""Tests for Gender API endpoint."""
import pytest
import json


class TestGenderAPI:
    """Test suite for /api/v1/gender endpoint."""

    def test_gender_api_female_name(self, client):
        """Test gender detection for a typical female name."""
        response = client.get('/api/v1/gender?name=Emily')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'gender' in data
        assert 'name' in data
        assert 'time' in data
        assert data['name'] == 'Emily'

    def test_gender_api_male_name(self, client):
        """Test gender detection for a male name."""
        response = client.get('/api/v1/gender?name=John')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'gender' in data
        assert data['name'] == 'John'

    def test_gender_api_missing_parameter(self, client):
        """Test API response when name parameter is missing."""
        response = client.get('/api/v1/gender')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'message' in data

    def test_gender_api_empty_name(self, client):
        """Test API response for empty name."""
        response = client.get('/api/v1/gender?name=')
        assert response.status_code == 400

    def test_gender_api_first_name_param(self, client):
        """Test using alternative 'first_name' parameter."""
        response = client.get('/api/v1/gender?first_name=Sarah')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Sarah'

    def test_gender_api_whitespace_handling(self, client):
        """Test that whitespace is handled correctly."""
        response = client.get('/api/v1/gender?name=  Anna  ')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'gender' in data

    def test_gender_view(self, client):
        """Test the demo page for gender API."""
        response = client.get('/gender')
        assert response.status_code == 200
        assert b'gender' in response.data.lower()
