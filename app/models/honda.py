from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class ModelResponse(BaseModel):
    """Response model for single year model query"""
    year: int = Field(..., description="Model year")
    models: List[str] = Field(..., description="List of Honda models")
    total_count: int = Field(..., description="Total number of models")
    
    class Config:
        schema_extra = {
            "example": {
                "year": 2016,
                "models": ["Accord", "Civic", "CR-V", "Pilot"],
                "total_count": 4
            }
        }

class YearRangeResponse(BaseModel):
    """Response model for year range model query"""
    start_year: int = Field(..., description="Starting year of range")
    end_year: int = Field(..., description="Ending year of range")
    yearly_data: Dict[int, List[str]] = Field(..., description="Models organized by year")
    total_unique_models: int = Field(..., description="Total unique models across all years")
    
    class Config:
        schema_extra = {
            "example": {
                "start_year": 2020,
                "end_year": 2022,
                "yearly_data": {
                    2020: ["Accord", "Civic"],
                    2021: ["Accord", "Civic", "Passport"],
                    2022: ["Accord", "Civic", "Passport"]
                },
                "total_unique_models": 3
            }
        }

class DiscontinuedResponse(BaseModel):
    """Response model for discontinued models analysis"""
    start_year: int = Field(..., description="Starting year of analysis")
    end_year: int = Field(..., description="Ending year of analysis")
    early_years_models_count: int = Field(..., description="Number of models in early years")
    recent_years_models_count: int = Field(..., description="Number of models in recent years")
    discontinued_models: List[str] = Field(..., description="List of discontinued models")
    discontinued_count: int = Field(..., description="Number of discontinued models")
    
    class Config:
        schema_extra = {
            "example": {
                "start_year": 2015,
                "end_year": 2025,
                "early_years_models_count": 155,
                "recent_years_models_count": 113,
                "discontinued_models": ["CR-Z", "Clarity", "Fit"],
                "discontinued_count": 3
            }
        }

class StatisticsResponse(BaseModel):
    """Response model for comprehensive statistics"""
    analysis_period: str = Field(..., description="Analysis period range")
    total_unique_models: int = Field(..., description="Total unique models in period")
    yearly_model_counts: Dict[int, int] = Field(..., description="Model counts per year")
    peak_year: Dict[str, int] = Field(..., description="Year with most models")
    lowest_year: Dict[str, int] = Field(..., description="Year with fewest models")
    average_models_per_year: float = Field(..., description="Average models per year")
    discontinued_models_count: int = Field(..., description="Total discontinued models")
    discontinued_models: List[str] = Field(..., description="Sample discontinued models")
    trend_analysis: Dict[str, List[int]] = Field(..., description="Growth and decline years")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Check timestamp")
    api_connectivity: str = Field(..., description="External API status")
    test_query_result: Optional[str] = Field(None, description="Test query result")
    error: Optional[str] = Field(None, description="Error message if any")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Year must be between 1990 and 2030"
            }
        }
