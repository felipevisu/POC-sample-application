pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        PIP_CACHE_DIR = "${WORKSPACE}/.cache/pip"
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Check Python') {
            steps {
                echo 'Checking Python installation...'
                script {
                    try {
                        sh 'python3 --version'
                        env.PYTHON_CMD = 'python3'
                    } catch (Exception e) {
                        try {
                            sh 'python --version'
                            env.PYTHON_CMD = 'python'
                        } catch (Exception e2) {
                            error "Neither python3 nor python found. Please install Python on the Jenkins agent."
                        }
                    }
                }
                echo "Using Python command: ${env.PYTHON_CMD}"
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    echo "Python version:"
                    ${PYTHON_CMD} --version
                    
                    echo "Creating virtual environment..."
                    ${PYTHON_CMD} -m venv venv
                    
                    echo "Activating virtual environment and installing dependencies..."
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    
                    echo "Installing production dependencies..."
                    pip install -r requirements.txt
                    
                    echo "Installing development dependencies..."
                    pip install -r requirements-dev.txt
                    
                    echo "Verifying installations..."
                    pip list | grep -E "(pytest|fastapi|uvicorn)"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --cov=. --cov-report=xml --cov-report=html --cov-report=term-missing --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    // Publish test results
                    script {
                        if (fileExists('test-results.xml')) {
                            junit 'test-results.xml'
                        }
                    }
                    
                    // Publish coverage report
                    script {
                        if (fileExists('htmlcov/index.html')) {
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
            }
        }
        
        stage('Run Application Test') {
            steps {
                echo 'Testing application startup...'
                sh '''
                    . venv/bin/activate
                    
                    echo "Starting application in background..."
                    python main.py &
                    APP_PID=$!
                    
                    echo "Waiting for application to start..."
                    sleep 10
                    
                    echo "Testing health endpoint..."
                    curl -f http://localhost:8000/health || (echo "Health check failed" && kill $APP_PID && exit 1)
                    
                    echo "Testing root endpoint..."
                    curl -f http://localhost:8000/ || (echo "Root endpoint failed" && kill $APP_PID && exit 1)
                    
                    echo "Stopping application..."
                    kill $APP_PID
                    
                    echo "Application test completed successfully!"
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security scans...'
                sh '''
                    . venv/bin/activate
                    
                    echo "Running Bandit security scan..."
                    bandit -r . -f json -o bandit-report.json || echo "Bandit scan completed with warnings"
                    
                    echo "Running Safety dependency check..."
                    safety check --json --output safety-report.json || echo "Safety check completed with warnings"
                    
                    echo "Security scan reports generated"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                    echo 'Security reports archived'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh '''
                # Kill any remaining Python processes
                pkill -f "python.*main.py" || true
                # Clean up virtual environment
                rm -rf venv
            '''
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
            echo 'All tests passed and application is working correctly.'
        }
        failure {
            echo 'Pipeline failed!'
            echo 'Check the logs above for detailed error information.'
        }
        unstable {
            echo 'Pipeline completed with warnings!'
            echo 'Some non-critical steps may have failed.'
        }
    }
}
