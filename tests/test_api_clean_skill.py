"""Tests for Clean Skill API endpoint."""

import json


class TestCleanSkillAPI:
    """Test suite for /api/v1/clean_skill endpoint."""

    def test_clean_skill_javascript(self, client):
        """Test cleaning JavaScript skill variations."""
        response = client.get("/api/v1/clean_skill?skill=JavaScript")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "raw" in data
        assert "cleaned" in data
        assert "time" in data

    def test_clean_skill_with_special_chars(self, client):
        """Test cleaning skills with special characters."""
        response = client.get("/api/v1/clean_skill?skill=Node.js")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["raw"] == "Node.js"
        assert data["cleaned"] != ""

    def test_clean_skill_missing_parameter(self, client):
        """Test API response when skill parameter is missing."""
        response = client.get("/api/v1/clean_skill")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_clean_skill_empty(self, client):
        """Test API response for empty skill."""
        response = client.get("/api/v1/clean_skill?skill=")
        assert response.status_code == 400

    def test_clean_skill_alias(self, client):
        """Test skill alias normalization."""
        response = client.get("/api/v1/clean_skill?skill=java script")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should normalize to a standard form
        assert data["cleaned"] != ""

    def test_clean_skill_view(self, client):
        """Test the demo page for clean skill API."""
        response = client.get("/clean_skill")
        assert response.status_code == 200
