import requests
from typing import Set, Dict
from fastapi import HTTPException
from app.core.config import settings

class HondaModelsService:
    """Service class for Honda models business logic"""
    
    def __init__(self):
        self.base_url = settings.NHTSA_BASE_URL
        self.make = settings.MAKE
        self.timeout = settings.REQUEST_TIMEOUT
    
    def get_models_for_year(self, year: int) -> Set[str]:
        """
        Get all Honda models for a given year from NHTSA API
        
        Args:
            year (int): The model year
            
        Returns:
            Set[str]: Set of model names for the given year
            
        Raises:
            HTTPException: If API request fails
        """
        try:
            url = f"{self.base_url}/make/{self.make}/modelyear/{year}?format=json"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract model names from the response
            models = set()
            if 'Results' in data and data['Results']:
                for result in data['Results']:
                    if 'Model_Name' in result and result['Model_Name']:
                        models.add(result['Model_Name'].strip())
            
            return models
            
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=504, 
                detail=f"Request timeout while fetching data for year {year}"
            )
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=502, 
                detail=f"Error fetching data for year {year}: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Internal error processing data for year {year}: {str(e)}"
            )
    
    def get_all_models_in_range(self, start_year: int, end_year: int) -> Dict[int, Set[str]]:
        """
        Get all Honda models for a range of years
        
        Args:
            start_year (int): Starting year
            end_year (int): Ending year (inclusive)
            
        Returns:
            Dict[int, Set[str]]: Dictionary mapping year to set of models
        """
        all_models = {}
        
        for year in range(start_year, end_year + 1):
            models = self.get_models_for_year(year)
            all_models[year] = models
        
        return all_models
    
    def find_discontinued_models(self, start_year: int, end_year: int) -> Dict:
        """
        Find discontinued Honda models based on the criteria
        
        Definition of discontinued: Any model that was sold at least once from 
        start_year to (end_year-2) but not sold in the last 2 years (end_year-1, end_year)
        
        Args:
            start_year (int): Starting year of analysis
            end_year (int): Ending year of analysis
            
        Returns:
            Dict: Dictionary containing analysis results
        """
        # Get all models for each year
        yearly_models = self.get_all_models_in_range(start_year, end_year)
        
        # Get models from all years except the last 2
        early_years_models = set()
        for year in range(start_year, end_year - 1):  # end_year - 2 years
            if year in yearly_models:
                early_years_models.update(yearly_models[year])
        
        # Get models from the last 2 years
        last_two_years_models = set()
        for year in range(end_year - 1, end_year + 1):  # Last 2 years
            if year in yearly_models:
                last_two_years_models.update(yearly_models[year])
        
        # Discontinued = models that existed in early years but not in last 2 years
        discontinued_models = early_years_models - last_two_years_models
        
        return {
            "early_years_models": early_years_models,
            "recent_years_models": last_two_years_models,
            "discontinued_models": discontinued_models,
            "yearly_models": yearly_models
        }
    
    def get_comprehensive_statistics(self, start_year: int, end_year: int) -> Dict:
        """
        Get comprehensive statistics about Honda models
        
        Args:
            start_year (int): Starting year for analysis
            end_year (int): Ending year for analysis
            
        Returns:
            Dict: Comprehensive statistics and analysis
        """
        yearly_models = self.get_all_models_in_range(start_year, end_year)
        
        # Calculate statistics
        yearly_counts = {}
        all_models = set()
        
        for year, models in yearly_models.items():
            yearly_counts[year] = len(models)
            all_models.update(models)
        
        # Find peak and lowest years
        peak_year = max(yearly_counts, key=yearly_counts.get)
        lowest_year = min(yearly_counts, key=yearly_counts.get)
        
        # Calculate average
        avg_models_per_year = sum(yearly_counts.values()) / len(yearly_counts) if yearly_counts else 0
        
        # Find discontinued models
        discontinued_result = self.find_discontinued_models(start_year, end_year)
        
        # Trend analysis
        growth_years = []
        decline_years = []
        
        for year in range(start_year + 1, end_year + 1):
            current_count = yearly_counts.get(year, 0)
            previous_count = yearly_counts.get(year - 1, 0)
            
            if current_count > previous_count:
                growth_years.append(year)
            elif current_count < previous_count:
                decline_years.append(year)
        
        return {
            "analysis_period": f"{start_year}-{end_year}",
            "total_unique_models": len(all_models),
            "yearly_model_counts": yearly_counts,
            "peak_year": {
                "year": peak_year,
                "model_count": yearly_counts[peak_year]
            },
            "lowest_year": {
                "year": lowest_year,
                "model_count": yearly_counts[lowest_year]
            },
            "average_models_per_year": round(avg_models_per_year, 1),
            "discontinued_models_count": len(discontinued_result["discontinued_models"]),
            "discontinued_models": sorted(list(discontinued_result["discontinued_models"]))[:10],
            "trend_analysis": {
                "growth_years": growth_years,
                "decline_years": decline_years
            }
        }
    
    def test_api_connectivity(self) -> Dict:
        """
        Test API connectivity with a simple request
        
        Returns:
            Dict: Test results
        """
        try:
            test_models = self.get_models_for_year(2020)
            return {
                "status": "healthy",
                "api_connectivity": "ok",
                "test_query_result": f"Found {len(test_models)} models for 2020"
            }
        except Exception as e:
            return {
                "status": "degraded", 
                "api_connectivity": "error",
                "error": str(e)
            }

# Create service instance
honda_service = HondaModelsService()
