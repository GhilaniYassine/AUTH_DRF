import requests
import json

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        
    def register_and_login(self):
        # Register user
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        print("Testing Registration...")
        response = requests.post(f"{BASE_URL}/register/", json=register_data)
        print(f"Registration Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Login
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        print("\nTesting Login...")
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']
            print("Login successful!")
        else:
            print(f"Login failed: {response.json()}")
    
    def get_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}
    
    def test_categories(self):
        print("\n=== Testing Categories ===")
        
        # Create category
        category_data = {"name": "Electronics", "description": "Electronic items"}
        response = requests.post(f"{BASE_URL}/categories/", json=category_data, headers=self.get_headers())
        print(f"Create Category Status: {response.status_code}")
        
        if response.status_code == 201:
            category = response.json()
            category_id = category['id']
            print(f"Created category: {category}")
            
            # Get category
            response = requests.get(f"{BASE_URL}/categories/{category_id}/", headers=self.get_headers())
            print(f"Get Category Status: {response.status_code}")
            print(f"Category details: {response.json()}")
            
            # List categories
            response = requests.get(f"{BASE_URL}/categories/", headers=self.get_headers())
            print(f"List Categories Status: {response.status_code}")
            print(f"Categories: {response.json()}")
            
            return category_id
        return None
    
    def test_products(self, category_id):
        print("\n=== Testing Products ===")
        
        if not category_id:
            print("No category available for product testing")
            return None
            
        # Create product
        product_data = {
            "name": "Test Smartphone",
            "description": "A test smartphone",
            "price": "599.99",
            "category": category_id,
            "stock_quantity": 10
        }
        
        response = requests.post(f"{BASE_URL}/products/", json=product_data, headers=self.get_headers())
        print(f"Create Product Status: {response.status_code}")
        
        if response.status_code == 201:
            product = response.json()
            product_id = product['id']
            print(f"Created product: {product}")
            
            # Get product
            response = requests.get(f"{BASE_URL}/products/{product_id}/", headers=self.get_headers())
            print(f"Get Product Status: {response.status_code}")
            
            # List products
            response = requests.get(f"{BASE_URL}/products/", headers=self.get_headers())
            print(f"List Products Status: {response.status_code}")
            
            return product_id
        return None
    
    def test_cart_operations(self, product_id):
        print("\n=== Testing Cart Operations ===")
        
        if not product_id:
            print("No product available for cart testing")
            return
            
        # Create cart
        response = requests.post(f"{BASE_URL}/carts/", json={}, headers=self.get_headers())
        print(f"Create Cart Status: {response.status_code}")
        
        if response.status_code == 201:
            cart = response.json()
            cart_id = cart['id']
            
            # Add item to cart
            cart_item_data = {
                "cart": cart_id,
                "product": product_id,
                "quantity": 2
            }
            
            response = requests.post(f"{BASE_URL}/cart-items/", json=cart_item_data, headers=self.get_headers())
            print(f"Add to Cart Status: {response.status_code}")
            
            # Get cart
            response = requests.get(f"{BASE_URL}/carts/{cart_id}/", headers=self.get_headers())
            print(f"Get Cart Status: {response.status_code}")
            print(f"Cart details: {response.json()}")
    
    def test_orders(self):
        print("\n=== Testing Orders ===")
        
        # Create order
        order_data = {
            "shipping_address": "123 Test Street, Test City",
            "phone_number": "+1234567890"
        }
        
        response = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=self.get_headers())
        print(f"Create Order Status: {response.status_code}")
        
        if response.status_code == 201:
            order = response.json()
            order_id = order['id']
            print(f"Created order: {order}")
            
            # Get order
            response = requests.get(f"{BASE_URL}/orders/{order_id}/", headers=self.get_headers())
            print(f"Get Order Status: {response.status_code}")
            
            # List orders
            response = requests.get(f"{BASE_URL}/orders/", headers=self.get_headers())
            print(f"List Orders Status: {response.status_code}")
    
    def run_all_tests(self):
        print("Starting API Tests...")
        
        self.register_and_login()
        
        if self.access_token:
            category_id = self.test_categories()
            product_id = self.test_products(category_id)
            self.test_cart_operations(product_id)
            self.test_orders()
        else:
            print("Cannot proceed with tests - authentication failed")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
