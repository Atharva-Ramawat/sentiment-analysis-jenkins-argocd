pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_USER = "atharvaramawat" 
        
        // Define the Tag and Git Credentials
        IMAGE_TAG = "v${BUILD_NUMBER}" 
        GIT_CREDENTIALS_ID = 'github-pat-token'

        BACKEND_IMAGE = "${DOCKER_USER}/sentiment-backend"
        FRONTEND_IMAGE = "${DOCKER_USER}/sentiment-frontend"
    }

    stages {
        stage('Build Backend') {
            // --- LOOP PROTECTION (Fixed Syntax) ---
            when {
                not { changelog '.*skip ci.*' }
            }
            steps {
                script {
                    echo "Building Backend Image: ${IMAGE_TAG}..."
                    dir('backend') {
                        sh "docker build -t $BACKEND_IMAGE:${IMAGE_TAG} ."
                    }
                }
            }
        }

        stage('Build Frontend') {
            // --- LOOP PROTECTION ---
            when {
                not { changelog '.*skip ci.*' }
            }
            steps {
                script {
                    echo "Building Frontend Image: ${IMAGE_TAG}..."
                    dir('frontend') {
                        sh "docker build -t $FRONTEND_IMAGE:${IMAGE_TAG} ."
                    }
                }
            }
        }

        stage('Login & Push') {
            // --- LOOP PROTECTION ---
            when {
                not { changelog '.*skip ci.*' }
            }
            steps {
                script {
                    echo 'Pushing Docker Images...'
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    
                    sh "docker push $BACKEND_IMAGE:${IMAGE_TAG}"
                    sh "docker push $FRONTEND_IMAGE:${IMAGE_TAG}"
                }
            }
        }

        stage('Update Manifests') {
            // --- LOOP PROTECTION ---
            when {
                not { changelog '.*skip ci.*' }
            }
            steps {
                script {
                    echo "Updating Kubernetes Deployment..."
                    sh 'git config user.email "jenkins@bot.com"'
                    sh 'git config user.name "Jenkins Bot"'

                    // Updates the deployment file with the new tag
                    sh "sed -i 's|image: ${FRONTEND_IMAGE}:.*|image: ${FRONTEND_IMAGE}:${IMAGE_TAG}|' deployment.yaml"
                    sh "sed -i 's|image: ${BACKEND_IMAGE}:.*|image: ${BACKEND_IMAGE}:${IMAGE_TAG}|' deployment.yaml"

                    withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                        sh "git add ."
                        sh "git commit -m 'Update images to ${IMAGE_TAG} [skip ci]'"
                        sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/Atharva-Ramawat/sentiment-analysis-jenkins-argocd.git HEAD:main"
                    }
                }
            }
        }

        stage('Cleanup') {
            // --- LOOP PROTECTION ---
            when {
                not { changelog '.*skip ci.*' }
            }
            steps {
                script {
                    echo 'Removing Local Images...'
                    sh "docker rmi $BACKEND_IMAGE:${IMAGE_TAG}"
                    sh "docker rmi $FRONTEND_IMAGE:${IMAGE_TAG}"
                }
            }
        }
    }
}