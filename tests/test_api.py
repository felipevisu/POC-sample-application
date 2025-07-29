import pytest
from fastapi.testclient import TestClient

from main import PRODUCTS, app

# Create a test client
client = TestClient(app)


class TestRootEndpoint:
    """Test cases for the root endpoint"""

    def test_root_endpoint(self):
        """Test the root endpoint returns correct information"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert data["message"] == "Welcome to Market Products API"
        assert "list_products" in data["endpoints"]
        assert "product_details" in data["endpoints"]
        assert "api_docs" in data["endpoints"]


class TestHealthEndpoint:
    """Test cases for the health check endpoint"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "API is running properly"


class TestProductsEndpoint:
    """Test cases for the products endpoints"""

    def test_list_all_products(self):
        """Test listing all products"""
        response = client.get("/products")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == len(PRODUCTS)
        assert isinstance(data, list)

        # Check if all products have required fields
        for product in data:
            assert "id" in product
            assert "name" in product
            assert "category" in product
            assert "price" in product
            assert "description" in product
            assert "in_stock" in product

    def test_filter_products_by_category(self):
        """Test filtering products by category"""
        response = client.get("/products?category=Fruits")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2  # We have 2 fruit products

        for product in data:
            assert product["category"] == "Fruits"

    def test_filter_products_by_stock(self):
        """Test filtering products by stock availability"""
        response = client.get("/products?in_stock=true")
        assert response.status_code == 200

        data = response.json()
        for product in data:
            assert product["in_stock"] is True

        # Test filtering for out of stock products
        response = client.get("/products?in_stock=false")
        assert response.status_code == 200

        data = response.json()
        for product in data:
            assert product["in_stock"] is False

    def test_filter_products_by_category_and_stock(self):
        """Test filtering products by both category and stock"""
        response = client.get("/products?category=Dairy&in_stock=true")
        assert response.status_code == 200

        data = response.json()
        for product in data:
            assert product["category"] == "Dairy"
            assert product["in_stock"] is True

    def test_filter_with_nonexistent_category(self):
        """Test filtering with a category that doesn't exist"""
        response = client.get("/products?category=NonExistent")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 0

    def test_case_insensitive_category_filter(self):
        """Test that category filtering is case insensitive"""
        response = client.get("/products?category=fruits")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 2  # Should still find the Fruits category


class TestProductDetailsEndpoint:
    """Test cases for the product details endpoint"""

    def test_get_existing_product(self):
        """Test getting details for an existing product"""
        product_id = 1
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Fresh Apples"
        assert data["category"] == "Fruits"
        assert "price" in data
        assert "description" in data
        assert "in_stock" in data

    def test_get_nonexistent_product(self):
        """Test getting details for a product that doesn't exist"""
        response = client.get("/products/999")
        assert response.status_code == 404

        data = response.json()
        assert data["detail"] == "Product not found"

    def test_get_all_products_individually(self):
        """Test that all products can be retrieved individually"""
        for product in PRODUCTS:
            response = client.get(f"/products/{product.id}")
            assert response.status_code == 200

            data = response.json()
            assert data["id"] == product.id
            assert data["name"] == product.name
            assert data["category"] == product.category

    def test_invalid_product_id_type(self):
        """Test handling of invalid product ID types"""
        response = client.get("/products/invalid")
        assert response.status_code == 422  # Validation error


class TestAPISchema:
    """Test cases for API schema validation"""

    def test_product_schema_validation(self):
        """Test that returned products match the expected schema"""
        response = client.get("/products")
        assert response.status_code == 200

        data = response.json()
        for product in data:
            # Test required fields
            assert isinstance(product["id"], int)
            assert isinstance(product["name"], str)
            assert isinstance(product["category"], str)
            assert isinstance(product["price"], (int, float))
            assert isinstance(product["description"], str)
            assert isinstance(product["in_stock"], bool)

            # Test value constraints
            assert product["id"] > 0
            assert len(product["name"]) > 0
            assert len(product["category"]) > 0
            assert product["price"] > 0
            assert len(product["description"]) > 0

    def test_openapi_docs_accessible(self):
        """Test that OpenAPI documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Market Products API"
