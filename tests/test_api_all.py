"""Tests for all other API endpoints."""
import pytest
import json
from unittest.mock import patch, Mock


class TestProfileFakerAPI:
    """Test suite for /api/v1/profile_faker endpoint."""

    def test_profile_faker_success(self, client):
        """Test profile faker generates data."""
        response = client.get('/api/v1/profile_faker')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'name' in data
        assert 'email' in data
        assert 'address' in data
        assert 'company' in data

    def test_profile_faker_view(self, client):
        """Test the demo page for profile faker."""
        response = client.get('/profile_faker')
        assert response.status_code == 200


class TestCleanDatetimeAPI:
    """Test suite for /api/v1/clean_datetime endpoint."""

    def test_clean_datetime_valid_date(self, client):
        """Test parsing a valid date."""
        response = client.get('/api/v1/clean_datetime?datetime=January 2020')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'raw' in data
        assert 'cleaned' in data
        assert '2020' in data['cleaned']

    def test_clean_datetime_missing_parameter(self, client):
        """Test missing datetime parameter."""
        response = client.get('/api/v1/clean_datetime')
        assert response.status_code == 400

    def test_clean_datetime_now(self, client):
        """Test NOW keyword."""
        response = client.get('/api/v1/clean_datetime?datetime=NOW')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['cleaned'] != ''

    def test_clean_datetime_view(self, client):
        """Test the demo page."""
        response = client.get('/clean_datetime')
        assert response.status_code == 200


class TestSimilarSkillAPI:
    """Test suite for /api/v1/similar_skill endpoint."""

    def test_similar_skill_stub(self, client):
        """Test similar skill (currently returns empty list)."""
        response = client.get('/api/v1/similar_skill?skill=python')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'similar_skills' in data
        assert isinstance(data['similar_skills'], list)

    def test_similar_skill_missing_parameter(self, client):
        """Test missing skill parameter."""
        response = client.get('/api/v1/similar_skill')
        assert response.status_code == 400


class TestHealthEndpoints:
    """Test suite for health and utility endpoints."""

    def test_ping(self, client):
        """Test ping endpoint."""
        response = client.get('/ping')
        assert response.status_code == 200
        assert b'PONG' in response.data

    def test_healthcheck(self, client):
        """Test health endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'version' in data

    def test_index(self, client):
        """Test index page."""
        response = client.get('/')
        assert response.status_code == 200

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data


class TestSecurityHeaders:
    """Test suite for security headers."""

    def test_security_headers_present(self, client):
        """Test that security headers are added to responses."""
        response = client.get('/health')
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        assert 'X-XSS-Protection' in response.headers
        assert 'Strict-Transport-Security' in response.headers

    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.get('/health')
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers
