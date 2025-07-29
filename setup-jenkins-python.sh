#!/bin/bash

# Jenkins Agent Python Setup Script
# This script helps set up Python on a Jenkins agent

echo "🔧 Jenkins Agent Python Setup"
echo "=============================="

# Check if we're running as root
if [[ $EUID -eq 0 ]]; then
   echo "ℹ️  Running as root - can install system packages"
   ROOT_ACCESS=true
else
   echo "ℹ️  Running as non-root user"
   ROOT_ACCESS=false
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check current Python installations
echo "📋 Checking current Python installations..."

if command_exists python3; then
    echo "✅ python3 found: $(python3 --version)"
    PYTHON3_AVAILABLE=true
else
    echo "❌ python3 not found"
    PYTHON3_AVAILABLE=false
fi

if command_exists python; then
    echo "✅ python found: $(python --version)"
    PYTHON_AVAILABLE=true
else
    echo "❌ python not found"
    PYTHON_AVAILABLE=false
fi

# Check pip
if command_exists pip3; then
    echo "✅ pip3 found: $(pip3 --version)"
elif command_exists pip; then
    echo "✅ pip found: $(pip --version)"
else
    echo "❌ pip not found"
fi

# If Python is not available, try to install it
if [[ "$PYTHON3_AVAILABLE" == false && "$PYTHON_AVAILABLE" == false ]]; then
    echo ""
    echo "🚨 Python not found! Attempting to install..."
    
    if [[ "$ROOT_ACCESS" == true ]]; then
        # Detect OS and install Python
        if command_exists apt-get; then
            echo "📦 Detected Debian/Ubuntu - installing Python..."
            apt-get update
            apt-get install -y python3 python3-pip python3-venv python3-dev
        elif command_exists yum; then
            echo "📦 Detected RHEL/CentOS - installing Python..."
            yum install -y python3 python3-pip python3-venv
        elif command_exists dnf; then
            echo "📦 Detected Fedora - installing Python..."
            dnf install -y python3 python3-pip python3-venv
        elif command_exists apk; then
            echo "📦 Detected Alpine - installing Python..."
            apk add --no-cache python3 py3-pip
        else
            echo "❌ Unknown package manager. Please install Python manually."
            exit 1
        fi
    else
        echo "❌ No root access. Please ask your Jenkins administrator to install Python."
        echo ""
        echo "Required packages:"
        echo "  - python3"
        echo "  - python3-pip"
        echo "  - python3-venv"
        echo "  - python3-dev (on Debian/Ubuntu)"
        exit 1
    fi
fi

# Verify installation
echo ""
echo "🔍 Verifying Python installation..."

if command_exists python3; then
    echo "✅ python3: $(python3 --version)"
    FINAL_PYTHON_CMD="python3"
elif command_exists python; then
    echo "✅ python: $(python --version)"
    FINAL_PYTHON_CMD="python"
else
    echo "❌ Python installation failed!"
    exit 1
fi

# Test virtual environment creation
echo ""
echo "🧪 Testing virtual environment creation..."
TEST_VENV_DIR="/tmp/jenkins_python_test_$$"

if $FINAL_PYTHON_CMD -m venv "$TEST_VENV_DIR"; then
    echo "✅ Virtual environment creation works"
    rm -rf "$TEST_VENV_DIR"
else
    echo "❌ Virtual environment creation failed"
    echo "This might be due to missing python3-venv package"
    exit 1
fi

# Test pip installation
echo ""
echo "🧪 Testing pip installation..."
if command_exists pip3; then
    pip3 --version
    echo "✅ pip3 is working"
elif command_exists pip; then
    pip --version
    echo "✅ pip is working"
else
    echo "❌ pip not found after installation"
    exit 1
fi

echo ""
echo "🎉 Python setup completed successfully!"
echo ""
echo "📋 Summary:"
echo "  - Python command: $FINAL_PYTHON_CMD"
echo "  - Virtual environment: ✅ Working"
echo "  - Pip: ✅ Working"
echo ""
echo "💡 Your Jenkins pipeline should now work with the updated Jenkinsfile"
echo ""
echo "🔧 If you're still having issues, you can:"
echo "  1. Use Jenkinsfile.no-docker (doesn't require Docker agent)"
echo "  2. Make sure Jenkins agent has these tools installed"
echo "  3. Contact your Jenkins administrator for system-level Python installation"
