#!/usr/bin/env python3
"""
Test script for Veefyed - Backend Technical Task
Demonstrates upload and analysis workflow
"""
import requests
import sys
from pathlib import Path

# Configuration
API_KEY = "veefyed-UV9tbAcqbFpk"
BASE_URL = "http://localhost:8000/api"
HEADERS = {"X-API-Key": API_KEY}


def test_health_check():
    """Test health check endpoint"""
    print("🏥 Testing health check...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def upload_image(image_path):
    """Upload an image"""
    print(f"📤 Uploading image: {image_path}")

    if not Path(image_path).exists():
        print(f"❌ Error: Image file not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            files = {"file": (Path(image_path).name, f, "image/jpeg")}
            response = requests.post(f"{BASE_URL}/upload", headers=HEADERS, files=files)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload successful!")
            print(f"   Image ID: {data['image_id']}")
            print(f"   Filename: {data['filename']}")
            print(f"   Status: {data['status']}")
            print()
            return data["image_id"]
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            print()
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def analyze_image(image_id):
    """Analyze an uploaded image"""
    print(f"🔍 Analyzing image: {image_id}")

    try:
        response = requests.post(
            f"{BASE_URL}/analyze", headers=HEADERS, json={"image_id": image_id}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis complete!")
            print(f"   Skin Type: {data['skin_type']}")
            print(f"   Issues: {', '.join(data['issues'])}")
            print(f"   Confidence: {data['confidence']:.2%}")
            print()
            return data
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            print()
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def test_invalid_api_key():
    """Test with invalid API key"""
    print("🔐 Testing invalid API key...")
    response = requests.post(
        f"{BASE_URL}/upload",
        headers={"X-API-Key": "invalid-key"},
        files={"file": ("test.jpg", b"fake data", "image/jpeg")},
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_missing_image():
    """Test analysis with non-existent image ID"""
    print("❓ Testing with non-existent image ID...")
    response = requests.post(
        f"{BASE_URL}/analyze", headers=HEADERS, json={"image_id": "non-existent-id"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def main():
    """Main test workflow"""
    print("=" * 60)
    print("Veefyed - Backend Technical Task - Test Script")
    print("=" * 60)
    print()

    # Test health check
    test_health_check()

    # Test with image file if provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]

        # Upload image
        image_id = upload_image(image_path)

        if image_id:
            # Analyze image
            analyze_image(image_id)
    else:
        print("ℹ️  No image provided. Testing error cases only.")
        print()

    # Test error cases
    print("Testing Error Handling:")
    print("-" * 60)
    test_invalid_api_key()
    test_missing_image()

    print("=" * 60)
    print("✅ All tests completed!")
    print()
    print("Usage: python test_api.py [path/to/image.jpg]")
    print("=" * 60)


if __name__ == "__main__":
    main()
