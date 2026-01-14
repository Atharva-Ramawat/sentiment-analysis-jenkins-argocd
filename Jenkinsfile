pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_USER = "atharvaramawat" 
        // Image names
        BACKEND_IMAGE = "${DOCKER_USER}/sentiment-backend"
        FRONTEND_IMAGE = "${DOCKER_USER}/sentiment-frontend"
    }

    stages {
        stage('Build Backend') {
            steps {
                script {
                    echo 'Building Backend Image...'
                    dir('backend') {
                        sh "docker build -t $BACKEND_IMAGE:latest ."
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    echo 'Building Frontend Image...'
                    dir('frontend') {
                        sh "docker build -t $FRONTEND_IMAGE:latest ."
                    }
                }
            }
        }

        stage('Login & Push') {
            steps {
                script {
                    echo 'Pushing Docker Images...'
                    // This uses the ID you just created to log in securely
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    
                    sh "docker push $BACKEND_IMAGE:latest"
                    sh "docker push $FRONTEND_IMAGE:latest"
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo 'Removing Local Images to save space...'
                    sh "docker rmi $BACKEND_IMAGE:latest"
                    sh "docker rmi $FRONTEND_IMAGE:latest"
                }
            }
        }
    }
}