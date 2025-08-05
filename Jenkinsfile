pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fastapi-app:test'
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo '🧪 Running tests inside container...'
                sh 'docker run --rm ${DOCKER_IMAGE} pytest tests/ -v --cov=. --cov-report=xml --cov-report=html --cov-report=term-missing --junitxml=test-results.xml'
            }
            post {
                always {
                    script {
                        if (fileExists('test-results.xml')) {
                            junit 'test-results.xml'
                        }
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

        stage('Run Application Container Test') {
            steps {
                echo '🌐 Starting container and testing HTTP endpoints...'
                script {
                    def containerId = sh(
                        script: "docker run -d -p 8000:8000 ${DOCKER_IMAGE}",
                        returnStdout: true
                    ).trim()

                    sleep 10

                    try {
                        sh 'curl -f http://localhost:8000/health'
                        sh 'curl -f http://localhost:8000/'
                    } catch (Exception e) {
                        sh "docker logs ${containerId}"
                        sh "docker stop ${containerId}"
                        error "❌ App failed health check"
                    }

                    sh "docker stop ${containerId}"
                }
            }
        }

        stage('Security Scan') {
            steps {
                echo '🔐 Running security scans in Docker...'
                sh '''
                    docker run --rm ${DOCKER_IMAGE} bandit -r . -f json -o bandit-report.json || echo "Bandit scan completed with warnings"
                    docker run --rm ${DOCKER_IMAGE} safety check --json --output safety-report.json || echo "Safety check completed with warnings"
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
            echo '🧹 Cleaning up workspace...'
            sh 'docker system prune -f || true'
            cleanWs()
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        unstable {
            echo '⚠️ Pipeline completed with warnings!'
        }
    }
}
