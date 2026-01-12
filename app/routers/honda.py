from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.models.honda import (
    ModelResponse, 
    YearRangeResponse, 
    DiscontinuedResponse, 
    StatisticsResponse, 
    HealthResponse,
    ErrorResponse
)
from app.services.honda_service import honda_service
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=dict, summary="API Information")
async def root():
    """Get API information and available endpoints"""
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.PROJECT_DESCRIPTION,
        "endpoints": {
            "GET /models/{year}": "Get Honda models for a specific year",
            "GET /models/range": "Get Honda models for a year range",
            "GET /models/discontinued": "Find discontinued Honda models",
            "GET /models/statistics": "Get comprehensive statistics",
            "GET /health": "Health check endpoint",
            "GET /docs": "Interactive API documentation"
        },
        "data_source": "NHTSA Vehicle Database",
        "github": "https://github.com/yourusername/honda-vehicle-api"
    }

@router.get(
    "/models/{year}", 
    response_model=ModelResponse,
    summary="Get Models for Year",
    description="Get all Honda models available for a specific year"
)
async def get_models_for_year(
    year: int
):
    """
    Get all Honda models for a specific year
    
    - **year**: Model year (e.g., 2016, 2020, 2025)
    
    Returns a list of all Honda models available for the specified year.
    """
    # Validate year range
    if year < settings.MIN_YEAR or year > settings.MAX_YEAR:
        raise HTTPException(
            status_code=400, 
            detail=f"Year must be between {settings.MIN_YEAR} and {settings.MAX_YEAR}"
        )
    try:
        models_set = honda_service.get_models_for_year(year)
        models_list = sorted(list(models_set))
        
        return ModelResponse(
            year=year,
            models=models_list,
            total_count=len(models_list)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get(
    "/models/range", 
    response_model=YearRangeResponse,
    summary="Get Models for Year Range",
    description="Get all Honda models for a range of years"
)
async def get_models_for_range(
    start_year: int = Query(..., description="Starting year", ge=settings.MIN_YEAR, le=settings.MAX_YEAR),
    end_year: int = Query(..., description="Ending year", ge=settings.MIN_YEAR, le=settings.MAX_YEAR)
):
    """
    Get all Honda models for a range of years
    
    - **start_year**: Starting year (inclusive)
    - **end_year**: Ending year (inclusive)
    
    Returns models organized by year with comprehensive statistics.
    Maximum range is limited to 15 years for performance.
    """
    # Validation
    if start_year > end_year:
        raise HTTPException(status_code=400, detail="start_year must be less than or equal to end_year")
    
    if end_year - start_year > settings.MAX_YEAR_RANGE:
        raise HTTPException(status_code=400, detail=f"Year range cannot exceed {settings.MAX_YEAR_RANGE} years")
    
    try:
        yearly_models = honda_service.get_all_models_in_range(start_year, end_year)
        
        # Convert sets to sorted lists for JSON serialization
        yearly_data = {}
        all_unique_models = set()
        
        for year, models_set in yearly_models.items():
            models_list = sorted(list(models_set))
            yearly_data[year] = models_list
            all_unique_models.update(models_set)
        
        return YearRangeResponse(
            start_year=start_year,
            end_year=end_year,
            yearly_data=yearly_data,
            total_unique_models=len(all_unique_models)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get(
    "/models/discontinued", 
    response_model=DiscontinuedResponse,
    summary="Find Discontinued Models",
    description="Identify Honda models that have been discontinued"
)
async def get_discontinued_models(
    start_year: int = Query(..., description="Starting year of analysis", ge=settings.MIN_YEAR, le=settings.MAX_YEAR),
    end_year: int = Query(..., description="Ending year of analysis", ge=settings.MIN_YEAR, le=settings.MAX_YEAR)
):
    """
    Find discontinued Honda models
    
    **Definition of discontinued:** Models that were sold at least once from 
    start_year to (end_year-2) but not sold in the last 2 years (end_year-1, end_year)
    
    - **start_year**: Starting year of analysis
    - **end_year**: Ending year of analysis
    
    **Example:** For analysis period 2015-2025:
    - Models must appear in years 2015-2023
    - But not appear in years 2024-2025
    
    Minimum analysis period is 3 years.
    """
    # Validation
    if start_year > end_year:
        raise HTTPException(status_code=400, detail="start_year must be less than or equal to end_year")
    
    if end_year - start_year < settings.MIN_DISCONTINUATION_RANGE:
        raise HTTPException(
            status_code=400, 
            detail=f"Year range must be at least {settings.MIN_DISCONTINUATION_RANGE} years for discontinuation analysis"
        )
    
    if end_year - start_year > settings.MAX_YEAR_RANGE:
        raise HTTPException(status_code=400, detail=f"Year range cannot exceed {settings.MAX_YEAR_RANGE} years")
    
    try:
        result = honda_service.find_discontinued_models(start_year, end_year)
        
        discontinued_list = sorted(list(result["discontinued_models"]))
        
        return DiscontinuedResponse(
            start_year=start_year,
            end_year=end_year,
            early_years_models_count=len(result["early_years_models"]),
            recent_years_models_count=len(result["recent_years_models"]),
            discontinued_models=discontinued_list,
            discontinued_count=len(discontinued_list)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get(
    "/models/statistics", 
    response_model=StatisticsResponse,
    summary="Get Comprehensive Statistics",
    description="Get detailed statistics and trends about Honda models"
)
async def get_models_statistics(
    start_year: int = Query(2015, description="Starting year for statistics", ge=settings.MIN_YEAR, le=settings.MAX_YEAR),
    end_year: int = Query(2025, description="Ending year for statistics", ge=settings.MIN_YEAR, le=settings.MAX_YEAR)
):
    """
    Get comprehensive statistics about Honda models
    
    - **start_year**: Starting year for analysis (default: 2015)
    - **end_year**: Ending year for analysis (default: 2025)
    
    **Returns detailed analysis including:**
    - Total unique models across all years
    - Year-by-year model counts
    - Peak and lowest years
    - Average models per year
    - Discontinued models analysis
    - Growth and decline trend analysis
    """
    # Validation
    if start_year > end_year:
        raise HTTPException(status_code=400, detail="start_year must be less than or equal to end_year")
    
    if end_year - start_year > settings.MAX_YEAR_RANGE:
        raise HTTPException(status_code=400, detail=f"Year range cannot exceed {settings.MAX_YEAR_RANGE} years")
    
    try:
        statistics = honda_service.get_comprehensive_statistics(start_year, end_year)
        
        return StatisticsResponse(**statistics)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get(
    "/health", 
    response_model=HealthResponse,
    summary="Health Check",
    description="Check API health and external service connectivity"
)
async def health_check():
    """
    Health check endpoint
    
    Tests:
    - API responsiveness
    - External NHTSA API connectivity
    - Basic functionality with test query
    """
    try:
        # Test API connectivity
        test_result = honda_service.test_api_connectivity()
        
        return HealthResponse(
            status=test_result["status"],
            timestamp=datetime.now().isoformat(),
            api_connectivity=test_result["api_connectivity"],
            test_query_result=test_result.get("test_query_result"),
            error=test_result.get("error")
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now().isoformat(),
            api_connectivity="error",
            error=str(e)
        )
