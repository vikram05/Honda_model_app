import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "api_connectivity" in data

def test_get_models_for_year_valid():
    """Test getting models for a valid year"""
    response = client.get("/models/2020")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2020
    assert "models" in data
    assert "total_count" in data
    assert isinstance(data["models"], list)
    assert data["total_count"] >= 0

def test_get_models_for_year_invalid():
    """Test getting models for an invalid year"""
    response = client.get("/models/1800")
    assert response.status_code == 422  # Validation error

def test_get_models_range_valid():
    """Test getting models for a valid year range"""
    response = client.get("/models/range?start_year=2020&end_year=2022")
    assert response.status_code == 200
    data = response.json()
    assert data["start_year"] == 2020
    assert data["end_year"] == 2022
    assert "yearly_data" in data
    assert "total_unique_models" in data

def test_get_models_range_invalid():
    """Test getting models for an invalid year range"""
    # Test start_year > end_year
    response = client.get("/models/range?start_year=2022&end_year=2020")
    assert response.status_code == 400

def test_get_discontinued_models_valid():
    """Test getting discontinued models for a valid range"""
    response = client.get("/models/discontinued?start_year=2015&end_year=2020")
    assert response.status_code == 200
    data = response.json()
    assert data["start_year"] == 2015
    assert data["end_year"] == 2020
    assert "discontinued_models" in data
    assert "discontinued_count" in data

def test_get_discontinued_models_invalid_range():
    """Test getting discontinued models for too small range"""
    response = client.get("/models/discontinued?start_year=2020&end_year=2021")
    assert response.status_code == 400

def test_get_statistics_valid():
    """Test getting statistics for a valid range"""
    response = client.get("/models/statistics?start_year=2020&end_year=2022")
    assert response.status_code == 200
    data = response.json()
    assert "analysis_period" in data
    assert "total_unique_models" in data
    assert "yearly_model_counts" in data
    assert "peak_year" in data
    assert "trend_analysis" in data

def test_nonexistent_endpoint():
    """Test accessing a nonexistent endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
