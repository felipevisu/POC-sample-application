pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        PIP_CACHE_DIR = "${WORKSPACE}/.cache/pip"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --cov=. --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    // Publish test results
                    junit 'test-results.xml'
                    
                    // Publish coverage report
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
        
        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                script {
                    def image = docker.build("market-products-api:${env.BUILD_NUMBER}")
                    
                    // Test the Docker container
                    echo 'Testing Docker container...'
                    sh '''
                        docker run -d -p 8000:8000 --name test-container market-products-api:${BUILD_NUMBER}
                        sleep 10
                        curl -f http://localhost:8000/health
                        docker stop test-container
                        docker rm test-container
                    '''
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security scans...'
                sh '''
                    . venv/bin/activate
                    pip install bandit safety
                    bandit -r . -f json -o bandit-report.json || true
                    safety check --json --output safety-report.json || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}