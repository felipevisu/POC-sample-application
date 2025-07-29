from unittest import TestCase

import pytest

from main import PRODUCTS, Product


class TestProductModel:
    """Test cases for the Product model"""

    def test_product_creation(self):
        """Test creating a product instance"""
        product = Product(
            id=999,
            name="Test Product",
            category="Test Category",
            price=9.99,
            description="Test description",
            in_stock=True,
        )

        assert product.id == 999
        assert product.name == "Test Product"
        assert product.category == "Test Category"
        assert product.price == 9.99
        assert product.description == "Test description"
        assert product.in_stock is True

    def test_product_validation(self):
        """Test product validation with invalid data"""
        with pytest.raises(ValueError):
            Product(
                id="invalid",  # Should be int
                name="Test Product",
                category="Test Category",
                price=9.99,
                description="Test description",
                in_stock=True,
            )

    def test_product_price_validation(self):
        """Test product price validation"""
        with pytest.raises(ValueError):
            Product(
                id=999,
                name="Test Product",
                category="Test Category",
                price="invalid",  # Should be float
                description="Test description",
                in_stock=True,
            )

    def test_product_boolean_validation(self):
        """Test product boolean validation"""
        with pytest.raises(ValueError):
            Product(
                id=999,
                name="Test Product",
                category="Test Category",
                price=9.99,
                description="Test description",
                in_stock="invalid",  # Should be bool
            )


class TestProductsData:
    """Test cases for the products data"""

    def test_products_data_exists(self):
        """Test that products data exists and is not empty"""
        assert PRODUCTS is not None
        assert len(PRODUCTS) > 0

    def test_products_have_unique_ids(self):
        """Test that all products have unique IDs"""
        product_ids = [product.id for product in PRODUCTS]
        assert len(product_ids) == len(set(product_ids))

    def test_products_have_valid_data(self):
        """Test that all products have valid data"""
        for product in PRODUCTS:
            assert isinstance(product.id, int)
            assert product.id > 0
            assert isinstance(product.name, str)
            assert len(product.name) > 0
            assert isinstance(product.category, str)
            assert len(product.category) > 0
            assert isinstance(product.price, (int, float))
            assert product.price > 0
            assert isinstance(product.description, str)
            assert len(product.description) > 0
            assert isinstance(product.in_stock, bool)

    def test_products_categories(self):
        """Test that products have expected categories"""
        categories = {product.category for product in PRODUCTS}
        expected_categories = {
            "Fruits",
            "Dairy",
            "Bakery",
            "Meat",
            "Seafood",
            "Vegetables",
        }

        # Check that we have products in various categories
        assert len(categories) > 1
        # Check that all categories are from our expected set
        assert categories.issubset(expected_categories)

    def test_products_stock_status(self):
        """Test that products have both in-stock and out-of-stock items"""
        in_stock_products = [p for p in PRODUCTS if p.in_stock]
        out_of_stock_products = [p for p in PRODUCTS if not p.in_stock]

        # We should have both in-stock and out-of-stock products for testing
        assert len(in_stock_products) > 0
        assert len(out_of_stock_products) > 0
