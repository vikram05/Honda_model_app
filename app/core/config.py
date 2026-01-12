from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Project information
    PROJECT_NAME: str = "Honda Vehicle Models API"
    PROJECT_DESCRIPTION: str = "API to analyze Honda vehicle models using NHTSA database"
    VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # External API settings
    NHTSA_BASE_URL: str = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeyear"
    MAKE: str = "honda"
    REQUEST_TIMEOUT: int = 10
    
    # API limits
    MAX_YEAR_RANGE: int = 15
    MIN_YEAR: int = 1990
    MAX_YEAR: int = 2030
    MIN_DISCONTINUATION_RANGE: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
