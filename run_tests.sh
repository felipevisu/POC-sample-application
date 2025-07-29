#!/bin/bash

# Test script for CI/CD pipeline
set -e

echo "🧪 Running tests for Market Products API"
echo "========================================"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run linting (optional - you can add flake8 or black later)
echo "🔍 Code quality checks..."
# flake8 main.py  # Uncomment when flake8 is added
# black --check main.py  # Uncomment when black is added

# Run tests with coverage
echo "🚀 Running tests..."
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=xml --cov-report=html

# Check test coverage threshold (optional)
echo "📊 Coverage report generated"
echo "✅ All tests completed successfully!"

# Optional: Run security checks
# echo "🔒 Security checks..."
# bandit -r . -f json  # Uncomment when bandit is added

echo "🎉 Test pipeline completed successfully!"
