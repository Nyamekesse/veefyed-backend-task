# Testing Guide

This guide provides detailed instructions for testing the Veefyed - Backend Technical Task.

## Quick Start Testing

### 1. Using the Test Script

The easiest way to test the API is using the provided Python test script:

```bash
# Install requests library if needed
pip install requests

# Run test script (without image - tests error cases only)
python test_api.py

# Run test script with an image
python test_api.py <path/to/your/image.jpg>
```

### 2. Using Swagger UI (Recommended)

1. Start the server
2. Open <http://localhost:8000/docs>
3. Click "Authorize" button
4. Enter API Key: `veefyed-UV9tbAcqbFpk`
5. Try the endpoints interactively

## Manual Testing

### Prerequisites

Make sure the server is running:

```bash
# Using run script
uvicorn app.main:app --reload
```

### Test 1: Health Check (No Auth Required)

```bash
curl http://localhost:8000/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "veefyed-backend-task",
  "version": "1.0.0"
}
```

### Test 2: Upload Image (Success)

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -F "file=@test_image.jpg"
```

**Expected Response:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "test_image.jpg",
  "status": "uploaded"
}
```

**Save the image_id for the next test!**

### Test 3: Analyze Image (Success)

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "YOUR_IMAGE_ID_HERE"}'
```

**Expected Response:**

```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation", "Acne"],
  "confidence": 0.87
}
```

## Error Case Testing

### Test 4: Missing API Key

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@test_image.jpg"
```

**Expected Response (401):**

```json
{
  "detail": "API key is required. Include 'X-API-Key' header."
}
```

### Test 5: Invalid API Key

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: wrong-key" \
  -F "file=@test_image.jpg"
```

**Expected Response (403):**

```json
{
  "detail": "Invalid API key"
}
```

### Test 6: Invalid File Type

Create a text file and try to upload it:

```bash
echo "test" > test.txt
curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -F "file=@test.txt"
```

**Expected Response (400):**

```json
{
  "detail": "Invalid file type. Allowed types: .jpg, .jpeg, .png"
}
```

### Test 7: File Too Large

```bash
# Create a 6MB file (exceeds 5MB limit)
dd if=/dev/zero of=large.jpg bs=1M count=6

curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -F "file=@large.jpg"
```

**Expected Response (400):**

```json
{
  "detail": "File size exceeds maximum allowed size of 5.0MB"
}
```

### Test 8: Non-existent Image ID

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "fake-id-12345"}'
```

**Expected Response (404):**

```json
{
  "detail": "Image not found: fake-id-12345"
}
```

### Test 9: Empty Image ID

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "X-API-Key: veefyed-UV9tbAcqbFpk" \
  -H "Content-Type: application/json" \
  -d '{"image_id": ""}'
```

**Expected Response (400):**

```json
{
  "detail": "image_id is required and cannot be empty"
}
```

## Python Testing Examples

### Example 1: Complete Workflow

```python
import requests
from pathlib import Path

API_KEY = "veefyed-UV9tbAcqbFpk"
BASE_URL = "http://localhost:8000/api"
HEADERS = {"X-API-Key": API_KEY}

# 1. Upload image
with open("test_image.jpg", "rb") as f:
    upload_response = requests.post(
        f"{BASE_URL}/upload",
        headers=HEADERS,
        files={"file": ("test_image.jpg", f, "image/jpeg")}
    )

print("Upload Response:", upload_response.json())
image_id = upload_response.json()["image_id"]

# 2. Analyze image
analyze_response = requests.post(
    f"{BASE_URL}/analyze",
    headers=HEADERS,
    json={"image_id": image_id}
)

print("Analysis Response:", analyze_response.json())
```

### Example 2: Error Handling

```python
import requests

API_KEY = "veefyed-UV9tbAcqbFpk"
BASE_URL = "http://localhost:8000/api"
HEADERS = {"X-API-Key": API_KEY}

def upload_and_analyze(image_path):
    try:
        # Upload
        with open(image_path, "rb") as f:
            upload_response = requests.post(
                f"{BASE_URL}/upload",
                headers=HEADERS,
                files={"file": f}
            )

        if upload_response.status_code != 200:
            print(f"Upload failed: {upload_response.json()}")
            return

        image_id = upload_response.json()["image_id"]

        # Analyze
        analyze_response = requests.post(
            f"{BASE_URL}/analyze",
            headers=HEADERS,
            json={"image_id": image_id}
        )

        if analyze_response.status_code == 200:
            result = analyze_response.json()
            print(f"Skin Type: {result['skin_type']}")
            print(f"Issues: {', '.join(result['issues'])}")
            print(f"Confidence: {result['confidence']}")
        else:
            print(f"Analysis failed: {analyze_response.json()}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Test
upload_and_analyze("test_image.jpg")
```

## Postman Collection

You can also test using Postman. Import this collection:

### 1. Upload Image

- **Method:** POST
- **URL:** <http://localhost:8000/api/upload>
- **Headers:**
  - X-API-Key: veefyed-UV9tbAcqbFpk
- **Body:** form-data
  - Key: file
  - Type: File
  - Value: [Select your image]

### 2. Analyze Image

- **Method:** POST
- **URL:** <http://localhost:8000/api/analyze>
- **Headers:**
  - X-API-Key: veefyed-UV9tbAcqbFpk
  - Content-Type: application/json
- **Body:** raw (JSON)

```json
{
  "image_id": "{{image_id}}"
}
```

## Checking Logs

The application logs all requests. Monitor logs while testing:

```bash
# Terminal output shows:
# - Request method and path
# - Response status code
# - Processing time
# - Validation errors
# - Storage operations
```
