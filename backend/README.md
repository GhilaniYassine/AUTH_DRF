# Beya Tech E-commerce Backend

A comprehensive Django REST API for an e-commerce platform built with Django Rest Framework.

## 🚀 Features

- **User Authentication**: Registration, login with JWT tokens
- **Product Management**: CRUD operations for products and categories
- **Secure API**: Token-based authentication for protected endpoints
- **Comprehensive Testing**: Unit tests and manual testing tools
- **Error Handling**: Proper validation and error responses
- **Documentation**: Detailed API documentation and testing guide

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Django TestCase, Coverage
- **API Documentation**: Manual testing scripts included

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd beya_tech/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## 🔧 API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test tests

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test tests
coverage report
```

For detailed testing instructions, see [README_TESTING.md](README_TESTING.md)

## 📝 Project Structure

```
backend/
├── beya_tech/          # Main project directory
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL configuration
│   └── wsgi.py         # WSGI configuration
├── apps/               # Django applications
│   ├── authentication/ # User auth app
│   ├── products/       # Products and categories
│   └── core/           # Core utilities
├── tests/              # Test files
├── requirements.txt    # Python dependencies
└── manage.py          # Django management script
```
