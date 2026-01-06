# Veefyed - Backend Technical Task

A FastAPI-based backend service for image upload and analysis, built for the Mobile Full-Stack Developer (Backend-Driven) role at Veefyed.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing the API](#testing-the-api)
- [Docker Deployment](#docker-deployment)
- [Design Decisions](#design-decisions)
- [Production Improvements](#production-improvements)

## Overview

This service provides two main endpoints:

1. **Upload Endpoint** - Accepts image uploads (JPEG/PNG, max 5MB), validates them, and stores them locally
2. **Analysis Endpoint** - Performs mock skin analysis on uploaded images and returns structured results

## Features

### Core Features (Required)

- Image upload with validation (file type and size)
- Local file storage system
- Mock analysis engine (skin type, issues, confidence scores)
- Comprehensive error handling
- Clean, maintainable code structure

### Bonus Features (Implemented)

- **API Key Authentication** - Secure endpoints with X-API-Key header
- **Logging System** - Request/response logging with timestamps
- **Dockerization** - Ready-to-deploy containerized application
- **Interactive API Docs** - Auto-generated Swagger UI
- **Health Check Endpoint** - Service monitoring

## Tech Stack

- **Language:** Python 3.13.3
- **Framework:** FastAPI
- **Async File Handling:** aiofiles
- **Validation:** Pydantic
- **Server:** Uvicorn (ASGI)
- **Containerization:** Docker

## Project Structure

```
veefyed-backend-task/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py           # Upload endpoint
│   │   └── analyze.py          # Analysis endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── image_service.py    # Image processing logic
│   │   └── analysis_service.py # Mock analysis logic
│   └── utils/
│       ├── __init__.py
│       ├── validators.py       # File validation utilities
│       ├── storage.py          # File storage utilities
│       └── auth.py             # API key authentication
├── uploads/                    # Local image storage directory
│   └── .gitkeep
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .dockerignore
├── .gitignore
└── README.md
```

## Setup & Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- (Optional) Docker for containerized deployment

### Local Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nyamekesse/veefyed-backend-task.git
   cd veefyed-backend-task
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Direct Python

```bash
uvicorn app.main:app --reload --port 8000
```

### Option 2: Using Python Module

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

- **Base URL:** <http://localhost:8000>
- **API Documentation:** <http://localhost:8000/docs>
- **Alternative Docs:** <http://localhost:8000/redoc>

## API Documentation

### Authentication

All endpoints (except `/health` and `/`) require API key authentication.

**Header:**

```
X-API-Key: veefyed-UV9tbAcqbFpk
```

### Endpoints

#### 1. Upload Image

**Endpoint:** `POST /api/upload`

**Description:** Upload an image for analysis

**Headers:**

```
X-API-Key: veefyed-UV9tbAcqbFpk
Content-Type: multipart/form-data
```

**Request:**

- **file** (form-data): Image file (JPEG or PNG, max 5MB)

**Response (200 OK):**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "sample.jpg",
  "status": "uploaded"
}
```

**Error Responses:**

- `400` - Invalid file type or size
- `401` - Missing API key
- `403` - Invalid API key
- `500` - Server error

---

#### 2. Analyze Image

**Endpoint:** `POST /api/analyze`

**Description:** Analyze an uploaded image

**Headers:**

```
X-API-Key: veefyed-UV9tbAcqbFpk
Content-Type: application/json
```

**Request Body:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200 OK):**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation", "Acne"],
  "confidence": 0.87
}
```

**Error Responses:**

- `400` - Invalid or missing image_id
- `401` - Missing API key
- `403` - Invalid API key
- `404` - Image not found
- `500` - Server error

---

#### 3. Health Check

**Endpoint:** `GET /health`

**Description:** Check service health (no authentication required)

**Response (200 OK):**

```json
{
  "status": "healthy",
  "service": "image-analysis-api",
  "version": "1.0.0"
}
```

## Testing the API

### Using Swagger UI

1. Navigate to <http://localhost:8000/docs>
2. Click "Authorize" and enter API key: `veefyed-UV9tbAcqbFpk`
3. Try the endpoints interactively

### Using Python

```python
import requests

API_KEY = "veefyed-UV9tbAcqbFpk"
BASE_URL = "http://localhost:8000/api"

# Upload image
with open("test_image.jpg", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload",
        headers={"X-API-Key": API_KEY},
        files={"file": f}
    )
    print(response.json())
    image_id = response.json()["image_id"]

# Analyze image
response = requests.post(
    f"{BASE_URL}/analyze",
    headers={"X-API-Key": API_KEY},
    json={"image_id": image_id}
)
print(response.json())
```

## Docker Deployment

### Build the Docker image

```bash
docker build -t veefyed-backend-task .
```

### Run the container

```bash
docker run -d \
  -p 8000:8000 \
  -e API_KEY=veefyed-UV9tbAcqbFpk \
  --name veefyed-backend \
  veefyed-backend-task
```

### Access the API

```bash
curl http://localhost:8000/health
```

### Stop the container

```bash
docker stop veefyed-backend
docker rm veefyed-backend
```

## Design Decisions

### 1. Architecture Pattern

- **Layered Architecture:** Separation of routes, services, and utilities
- **Single Responsibility:** Each module has a clear, focused purpose
- **Dependency Injection:** Services and utilities are injected where needed

### 2. Mock Analysis Logic

The analysis service uses a deterministic random seeding approach:

- Same `image_id` always produces same results (consistency)
- Simulates realistic AI behavior without actual ML models
- Easy to extend with real ML integration later

### 3. File Storage Strategy

- UUID-based filenames prevent collisions
- Original extensions preserved for compatibility
- Simple filesystem approach (suitable for development/demo)

### 4. Error Handling

- Validation at entry points (routes)
- Business logic errors in services
- Structured error responses with meaningful messages
- Comprehensive logging for debugging

### 5. Security

- API key authentication (simple but effective)
- File size and type validation
- No sensitive data in logs
- CORS configured (adjust for production)

## Production Improvements

If this were a production system, I would implement:

### 1. **Storage**

- Cloud storage (AWS S3, Google Cloud Storage)
- CDN for image delivery
- Database for metadata (PostgreSQL)
- Image optimization and thumbnails

### 2. **Security**

- JWT-based authentication with refresh tokens
- Rate limiting per user/IP
- Input sanitization and validation
- HTTPS enforcement
- API key rotation mechanism
- Helmet/security headers

### 3. **Scalability**

- Horizontal scaling with load balancer
- Async task queue (Celery/Redis) for analysis
- Database connection pooling
- Caching layer (Redis) for frequent queries
- Message queue for decoupled processing

### 4. **Monitoring & Observability**

- Prometheus metrics
- Grafana dashboards
- Error tracking (Sentry)
- Structured logging (JSON format)
- Health check endpoints with detailed status

### 5. **Testing**

- Unit tests (pytest)
- Integration tests
- Load testing (Locust/k6)
- CI/CD pipeline (GitHub Actions)

### 6. **Real AI Integration**

- ML model serving (TensorFlow Serving, TorchServe)
- Model versioning and A/B testing
- Preprocessing pipeline
- Post-processing and result formatting
- Model performance monitoring

### 7. **API Enhancements**

- Versioning (v1, v2)
- Pagination for list endpoints
- Filtering and sorting
- Webhooks for async results
- Batch processing endpoints
- WebSocket for real-time updates

### 8. **Data Management**

- Data retention policies
- Automated backups
- GDPR compliance (data deletion)
- Audit logging
- Data encryption at rest

### 9. **Documentation**

- OpenAPI 3.0 specification
- Postman collection
- Architecture diagrams
- Deployment guides
- Runbooks for operations

## Assumptions Made

1. **Image Format:** JPEG and PNG are sufficient for the use case
2. **File Size:** 5MB limit is reasonable for mobile uploads
3. **Analysis Delay:** Synchronous analysis is acceptable (typically would be async)
4. **Storage:** Local filesystem is suitable for development/testing
5. **Authentication:** Simple API key is sufficient for technical task
6. **Concurrency:** Single instance can handle expected load for demo
7. **Error Handling:** Standard HTTP status codes are clear enough
8. **Logging:** Console output is sufficient for development

## Notes

- The mock analysis uses deterministic randomization for consistency
- Same image always gets same analysis results (based on image_id hash)
- Uploaded images are stored in the `uploads/` directory
- API key can be changed via `API_KEY` environment variable
- All endpoints except health check require authentication
- The service logs all requests and responses for debugging

## 👤 Author

Developed as a technical assessment for the Mobile Full-Stack Developer (Backend-Driven) role at Veefyed.

---

**Time Invested:** ~4-5 hours (as per task guidelines)

**Features Delivered:**

- All core requirements
- All bonus features
- Production-quality code structure
- Comprehensive documentation
