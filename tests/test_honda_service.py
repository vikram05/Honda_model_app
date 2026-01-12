import pytest
from unittest.mock import Mock, patch
from app.services.honda_service import HondaModelsService

@pytest.fixture
def honda_service():
    """Create a Honda service instance for testing"""
    return HondaModelsService()

@pytest.fixture
def mock_requests_get():
    """Mock requests.get for testing"""
    with patch('app.services.honda_service.requests.get') as mock_get:
        yield mock_get

def test_get_models_for_year_success(honda_service, mock_requests_get):
    """Test successful API call for getting models"""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "Results": [
            {"Model_Name": "Accord"},
            {"Model_Name": "Civic"},
            {"Model_Name": "CR-V"}
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response
    
    # Test
    result = honda_service.get_models_for_year(2020)
    
    # Assertions
    assert len(result) == 3
    assert "Accord" in result
    assert "Civic" in result
    assert "CR-V" in result

def test_get_models_for_year_empty_response(honda_service, mock_requests_get):
    """Test API call with empty results"""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {"Results": []}
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response
    
    # Test
    result = honda_service.get_models_for_year(2020)
    
    # Assertions
    assert len(result) == 0

def test_get_all_models_in_range(honda_service, mock_requests_get):
    """Test getting models for a range of years"""
    # Mock response for different years
    def mock_response_factory(year):
        mock_response = Mock()
        if year == 2020:
            mock_response.json.return_value = {
                "Results": [{"Model_Name": "Accord"}, {"Model_Name": "Civic"}]
            }
        elif year == 2021:
            mock_response.json.return_value = {
                "Results": [{"Model_Name": "Accord"}, {"Model_Name": "Pilot"}]
            }
        else:
            mock_response.json.return_value = {"Results": []}
        mock_response.raise_for_status.return_value = None
        return mock_response
    
    # Configure mock to return different responses based on URL
    def side_effect(*args, **kwargs):
        url = args[0]
        if "2020" in url:
            return mock_response_factory(2020)
        elif "2021" in url:
            return mock_response_factory(2021)
        return mock_response_factory(0)
    
    mock_requests_get.side_effect = side_effect
    
    # Test
    result = honda_service.get_all_models_in_range(2020, 2021)
    
    # Assertions
    assert len(result) == 2
    assert 2020 in result
    assert 2021 in result
    assert len(result[2020]) == 2
    assert len(result[2021]) == 2

def test_find_discontinued_models(honda_service, mock_requests_get):
    """Test finding discontinued models"""
    # Mock response for different years
    def side_effect(*args, **kwargs):
        url = args[0]
        mock_response = Mock()
        
        if "2018" in url or "2019" in url:
            # Early years - include discontinued model
            mock_response.json.return_value = {
                "Results": [
                    {"Model_Name": "Accord"},
                    {"Model_Name": "Civic"},
                    {"Model_Name": "Discontinued_Model"}
                ]
            }
        elif "2020" in url or "2021" in url:
            # Recent years - exclude discontinued model
            mock_response.json.return_value = {
                "Results": [
                    {"Model_Name": "Accord"},
                    {"Model_Name": "Civic"}
                ]
            }
        else:
            mock_response.json.return_value = {"Results": []}
        
        mock_response.raise_for_status.return_value = None
        return mock_response
    
    mock_requests_get.side_effect = side_effect
    
    # Test
    result = honda_service.find_discontinued_models(2018, 2021)
    
    # Assertions
    assert "discontinued_models" in result
    assert "Discontinued_Model" in result["discontinued_models"]
    assert "Accord" not in result["discontinued_models"]  # Still available in recent years

def test_comprehensive_statistics(honda_service, mock_requests_get):
    """Test comprehensive statistics calculation"""
    # Mock consistent response
    mock_response = Mock()
    mock_response.json.return_value = {
        "Results": [{"Model_Name": "Accord"}, {"Model_Name": "Civic"}]
    }
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response
    
    # Test
    result = honda_service.get_comprehensive_statistics(2020, 2022)
    
    # Assertions
    assert "analysis_period" in result
    assert "total_unique_models" in result
    assert "yearly_model_counts" in result
    assert "peak_year" in result
    assert "trend_analysis" in result
    assert result["analysis_period"] == "2020-2022"

def test_api_connectivity_test(honda_service, mock_requests_get):
    """Test API connectivity test method"""
    # Mock successful response
    mock_response = Mock()
    mock_response.json.return_value = {
        "Results": [{"Model_Name": "Accord"}, {"Model_Name": "Civic"}]
    }
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response
    
    # Test
    result = honda_service.test_api_connectivity()
    
    # Assertions
    assert result["status"] == "healthy"
    assert result["api_connectivity"] == "ok"
    assert "test_query_result" in result
