# Honda Vehicle Models API

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern REST API built with FastAPI to analyze Honda vehicle models using the NHTSA (National Highway Traffic Safety Administration) database.

## 🚀 Features

- **📊 Model Analysis**: Get Honda models for any year or year range
- **🔍 Discontinuation Detection**: Identify discontinued models based on sales patterns
- **📈 Statistics & Trends**: Comprehensive analysis with insights
- **⚡ Fast & Async**: Built with FastAPI for high performance
- **📚 Auto Documentation**: Interactive API docs with Swagger UI
- **🛡️ Error Handling**: Robust error handling and validation
- **🏥 Health Monitoring**: Built-in health check endpoints

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/models/{year}` | Get models for specific year |
| `GET` | `/models/range` | Get models for year range |
| `GET` | `/models/discontinued` | Find discontinued models |
| `GET` | `/models/statistics` | Comprehensive statistics |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive API documentation |

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip or poetry

### Clone Repository
```bash
git clone https://github.com/vikram05/Honda_model_app.git
cd Honda_model_app
```

### Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📖 Usage Examples

### Get Models for 2016
```bash
curl "http://localhost:8000/models/2016"
```

### Get Models for Range (2020-2023)
```bash
curl "http://localhost:8000/models/range?start_year=2020&end_year=2023"
```

### Find Discontinued Models (2015-2025)
```bash
curl "http://localhost:8000/models/discontinued?start_year=2015&end_year=2025"
```

### Get Statistics
```bash
curl "http://localhost:8000/models/statistics?start_year=2015&end_year=2025"
```

## 🏗️ Project Structure

```
honda_vehicle_api/
│
├── app/                    # Application package
│   ├── __init__.py
│   ├── main.py            # FastAPI app instance
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   └── config.py      # Configuration settings
│   ├── models/            # Pydantic models
│   │   ├── __init__.py
│   │   └── honda.py       # Honda model schemas
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── honda_service.py
│   └── routers/           # API routes
│       ├── __init__.py
│       └── honda.py       # Honda endpoints
│
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_main.py
│   └── test_honda_service.py
│
├── docs/                  # Documentation
│   └── API_GUIDE.md
│
├── scripts/               # Utility scripts
│   └── run_tests.py
│
├── requirements.txt       # Dependencies
├── README.md             # This file
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── Dockerfile            # Docker configuration
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🐳 Docker Support

### Build Image
```bash
docker build -t honda-vehicle-api .
```

### Run Container
```bash
docker run -p 8000:8000 honda-vehicle-api
```

## 📊 Key Business Insights

### Discontinued Models Analysis (2015-2025)
- **53 models discontinued** out of 155 total models
- **Notable discontinuations**: CR-Z, Clarity, Fit (US market)
- **Strategy shift**: Focus on SUVs and hybrid/electric vehicles

### Market Trends
- **Peak year**: 2022 with 121 models
- **Recent consolidation**: 2023-2025 showing portfolio streamlining
- **Category shifts**: Reduced sedans, increased SUV/crossover focus

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 External APIs

This project uses the [NHTSA Vehicle API](https://vpic.nhtsa.dot.gov/api/) for vehicle data:
- Base URL: `https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeyear`
- No authentication required
- Rate limiting: Respectful usage recommended

## 📞 Contact

- **GitHub**: [@vikram05](https://github.com/vikram05)
- **Email**: your.email@example.com

## ⭐ Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the amazing web framework
- [NHTSA](https://www.nhtsa.gov/) for providing the vehicle database API
- [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation

---

**Built with ❤️ using FastAPI**
