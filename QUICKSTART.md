# Quick Start Guide

## Option 1: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
uvicorn app.main:app --reload
```

## Option 2: Docker

```bash
# Build and run
docker-compose up --build

# Or manually
docker build -t veefyed-backend-task .
docker run -p 8000:8000 veefyed-backend-task
```

## Test It

### Open your browser

- **API Docs:** <http://localhost:8000/docs>
- **Health Check:** <http://localhost:8000/health>

### Or use the test script

```bash
# Install requests
pip install requests

# Run tests
python test_api.py <path/to/image.jpg>
```

## Important Info

- **API Key:** `veefyed-UV9tbAcqbFpk`
- **Port:** 8000
- **Allowed files:** JPG, PNG (max 5MB)
- **Interactive docs:** <http://localhost:8000/docs>

## Need Help?

- Full documentation: [README.md](README.md)
- Testing guide: [TESTING.md](TESTING.md)
- Check logs in terminal for errors

## Common Issues

**Port already in use?**

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Module not found?**

```bash
# Make sure dependencies are installed
pip install -r requirements.txt
```

**Permission denied on uploads/?**

```bash
mkdir uploads
chmod 755 uploads
```

---
