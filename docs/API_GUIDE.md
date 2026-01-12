# Honda Vehicle Models API - Comprehensive Guide

## 🎯 API Overview

This API provides comprehensive analysis of Honda vehicle models using the NHTSA database. Perfect for automotive research, market analysis, and business intelligence.

## 📡 Base URL
```
https://your-api-domain.com
```

## 🔗 Quick Start

### 1. Health Check
```bash
curl "https://your-api-domain.com/health"
```

### 2. Get Models for Specific Year
```bash
curl "https://your-api-domain.com/models/2020"
```

### 3. Interactive Documentation
Visit: `https://your-api-domain.com/docs`

## 📋 Detailed Endpoints

### 🏠 Root Information
**GET /** - Get API information and available endpoints

**Response:**
```json
{
  "message": "Honda Vehicle Models API",
  "version": "1.0.0",
  "description": "API to analyze Honda vehicle models using NHTSA database",
  "endpoints": {...}
}
```

### 📅 Single Year Analysis
**GET /models/{year}** - Get all Honda models for a specific year

**Parameters:**
- `year` (path): Model year (1990-2030)

**Example:**
```bash
curl "https://your-api-domain.com/models/2016"
```

**Response:**
```json
{
  "year": 2016,
  "models": ["Accord", "Civic", "CR-V", "Pilot", ...],
  "total_count": 93
}
```

### 📊 Year Range Analysis
**GET /models/range** - Get Honda models for a range of years

**Parameters:**
- `start_year` (query): Starting year (1990-2030)
- `end_year` (query): Ending year (1990-2030)

**Example:**
```bash
curl "https://your-api-domain.com/models/range?start_year=2020&end_year=2023"
```

**Response:**
```json
{
  "start_year": 2020,
  "end_year": 2023,
  "yearly_data": {
    "2020": ["Accord", "Civic", ...],
    "2021": ["Accord", "Civic", ...],
    ...
  },
  "total_unique_models": 112
}
```

### 🔍 Discontinued Models Analysis
**GET /models/discontinued** - Find discontinued Honda models

**Definition:** Models present in early years but absent in the last 2 years of the analysis period.

**Parameters:**
- `start_year` (query): Starting year of analysis
- `end_year` (query): Ending year of analysis

**Example:**
```bash
curl "https://your-api-domain.com/models/discontinued?start_year=2015&end_year=2025"
```

**Response:**
```json
{
  "start_year": 2015,
  "end_year": 2025,
  "early_years_models_count": 155,
  "recent_years_models_count": 113,
  "discontinued_models": ["CR-Z", "Clarity", "Fit", ...],
  "discontinued_count": 53
}
```

### 📈 Comprehensive Statistics
**GET /models/statistics** - Get detailed statistics and trends

**Parameters:**
- `start_year` (query, optional): Starting year (default: 2015)
- `end_year` (query, optional): Ending year (default: 2025)

**Example:**
```bash
curl "https://your-api-domain.com/models/statistics?start_year=2015&end_year=2025"
```

**Response:**
```json
{
  "analysis_period": "2015-2025",
  "total_unique_models": 155,
  "yearly_model_counts": {
    "2015": 85,
    "2016": 93,
    ...
  },
  "peak_year": {"year": 2022, "model_count": 121},
  "lowest_year": {"year": 2025, "model_count": 84},
  "average_models_per_year": 98.7,
  "discontinued_models_count": 53,
  "discontinued_models": ["CR-Z", "Clarity", ...],
  "trend_analysis": {
    "growth_years": [2016, 2017, ...],
    "decline_years": [2023, 2024, ...]
  }
}
```

### 🏥 Health Check
**GET /health** - API health and connectivity status

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-12T10:30:00",
  "api_connectivity": "ok",
  "test_query_result": "Found 106 models for 2020"
}
```

## 📝 Request Examples

### Python
```python
import requests

# Get models for 2020
response = requests.get("https://your-api-domain.com/models/2020")
data = response.json()
print(f"Found {data['total_count']} models for {data['year']}")

# Find discontinued models
response = requests.get(
    "https://your-api-domain.com/models/discontinued",
    params={"start_year": 2015, "end_year": 2025}
)
data = response.json()
print(f"Discontinued: {data['discontinued_count']} models")
```

### JavaScript
```javascript
// Get comprehensive statistics
fetch('https://your-api-domain.com/models/statistics?start_year=2015&end_year=2025')
  .then(response => response.json())
  .then(data => {
    console.log(`Peak year: ${data.peak_year.year} with ${data.peak_year.model_count} models`);
    console.log(`Discontinued models: ${data.discontinued_models_count}`);
  });
```

### cURL
```bash
# Get year range with jq formatting
curl -s "https://your-api-domain.com/models/range?start_year=2020&end_year=2022" \
  | jq '.yearly_data | keys[]'

# Health check
curl -s "https://your-api-domain.com/health" | jq '.status'
```

## 🚨 Error Handling

### Common Error Responses

**400 Bad Request** - Invalid parameters
```json
{
  "error": "Validation Error",
  "detail": "start_year must be less than or equal to end_year"
}
```

**422 Unprocessable Entity** - Validation error
```json
{
  "error": "Validation Error",
  "detail": "Year must be between 1990 and 2030"
}
```

**500 Internal Server Error** - Server error
```json
{
  "error": "Internal server error",
  "detail": "An unexpected error occurred"
}
```

**502 Bad Gateway** - External API error
```json
{
  "error": "External API Error",
  "detail": "Error fetching data for year 2020: Connection timeout"
}
```

## ⚡ Rate Limiting & Best Practices

### Recommendations:
- **Batch Requests**: Use year ranges instead of individual year calls
- **Cache Results**: API data is relatively stable, cache for reasonable periods
- **Error Handling**: Always handle network timeouts and API errors
- **Respectful Usage**: Don't exceed 10 requests per second

### Optimal Usage Patterns:
```python
# ✅ Good - Single range request
models = get_models_range(2015, 2025)

# ❌ Avoid - Multiple individual requests
for year in range(2015, 2026):
    models = get_models_for_year(year)  # Too many requests
```

## 📊 Business Use Cases

### Market Analysis
```python
# Analyze Honda's product strategy
stats = get_statistics(2015, 2025)
print(f"Portfolio evolution: {stats['peak_year']} was peak with {stats['peak_year']['model_count']} models")
print(f"Recent consolidation: {stats['discontinued_models_count']} models discontinued")
```

### Competitive Intelligence
```python
# Identify discontinued segments
discontinued = get_discontinued_models(2015, 2025)
segments = categorize_models(discontinued['discontinued_models'])
print(f"Honda exited these segments: {segments}")
```

### Historical Research
```python
# Decade comparison
models_2000s = get_models_range(2000, 2009)
models_2010s = get_models_range(2010, 2019)
models_2020s = get_models_range(2020, 2025)
```

## 🔧 Integration Examples

### Dashboard Integration
```javascript
// Real-time Honda model tracker
async function updateDashboard() {
  const health = await fetch('/health').then(r => r.json());
  const stats = await fetch('/models/statistics').then(r => r.json());
  
  updateHealthStatus(health.status);
  updateModelCount(stats.total_unique_models);
  updateTrends(stats.trend_analysis);
}
```

### Data Pipeline
```python
# ETL process for automotive database
def extract_honda_data():
    api_client = HondaAPIClient()
    
    # Extract current model lineup
    current_models = api_client.get_models_for_year(2025)
    
    # Extract historical trends
    trends = api_client.get_statistics(2015, 2025)
    
    # Extract discontinuation patterns
    discontinued = api_client.get_discontinued_models(2015, 2025)
    
    return {
        'current': current_models,
        'trends': trends,
        'discontinued': discontinued
    }
```

## 📈 Data Insights

### Key Findings (2015-2025):
- **155 unique models** across the analysis period
- **Peak year**: 2022 with 121 models
- **53 models discontinued** (34% discontinuation rate)
- **Notable exits**: CR-Z, Clarity, Fit (US market)
- **Strategy shift**: Sedan reduction, SUV/hybrid focus

### Trend Analysis:
- **Growth phase**: 2015-2022 (expanding portfolio)
- **Consolidation phase**: 2023-2025 (streamlining focus)
- **Market adaptation**: Response to consumer preferences

---

**📧 Support**: api-support@yourdomain.com  
**📖 Documentation**: https://your-api-domain.com/docs  
**🔗 GitHub**: https://github.com/yourusername/honda-vehicle-api
