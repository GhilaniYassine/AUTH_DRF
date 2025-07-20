
# API Testing Guide

## Running Django Unit Tests

1. **Run all tests:**
   ```bash
   python manage.py test tests
   ```

2. **Run specific test file:**
   ```bash
   python manage.py test tests.test_auth
   python manage.py test tests.test_models
   ```

3. **Run with coverage (install coverage first):**
   ```bash
   pip install coverage
   coverage run --source='.' manage.py test tests
   coverage report
   coverage html  # Creates htmlcov/index.html
   ```

## Manual API Testing

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Run manual API tests:**
   ```bash
   pip install requests  # if not already installed
   python test_api_manual.py
   ```

## Using curl for Quick Tests

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Categories (replace TOKEN with actual token)
```bash
# Create category
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Electronics","description":"Electronic items"}'

# List categories
curl -X GET http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer TOKEN"
```

### Products
```bash
# Create product (replace CATEGORY_ID)
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"name":"Smartphone","description":"Latest smartphone","price":"599.99","category":CATEGORY_ID,"stock_quantity":10}'
```

## Using Postman

1. Import the following environment variables:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (set after login)

2. Create requests for each endpoint with proper authentication headers.

## Test Data Cleanup

To reset test data:
```bash
python manage.py flush --noinput
python manage.py migrate
```
