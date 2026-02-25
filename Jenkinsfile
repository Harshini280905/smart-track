// ─────────────────────────────────────────────────────────────────────────────
// SmartTrack — Jenkinsfile
// CI/CD Pipeline with 4 Stages
// Stage 1: Clone  |  Stage 2: Build & Test  |  Stage 3: Docker Build & Push
// Stage 4 (Nice to Have): Deploy to AWS EC2
// ─────────────────────────────────────────────────────────────────────────────

pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')   // Jenkins credential ID
        DOCKERHUB_USERNAME    = 'your-dockerhub-username'              // Replace with your DockerHub username
        IMAGE_NAME            = 'smarttrack-app'
        IMAGE_TAG             = "${env.BUILD_NUMBER}"
        EC2_HOST              = 'ec2-user@<your-ec2-public-ip>'        // Replace with your EC2 IP
        EC2_SSH_KEY           = credentials('ec2-ssh-key')             // Jenkins credential ID for EC2 key
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        // ── STAGE 1: CLONE ────────────────────────────────────────────────────
        stage('Stage 1: Clone Repository') {
            steps {
                echo '========== Cloning repository from GitHub =========='
                checkout scm
                sh '''
                    echo "Repository cloned successfully"
                    echo "Branch: ${GIT_BRANCH}"
                    echo "Commit: ${GIT_COMMIT}"
                    ls -la
                '''
            }
        }

        // ── STAGE 2: BUILD & TEST ─────────────────────────────────────────────
        stage('Stage 2: Build & Test') {
            steps {
                echo '========== Installing dependencies and running tests =========='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt

                    echo "--- Running Unit Tests ---"
                    python -m pytest tests/ -v --tb=short

                    echo "--- Linting with flake8 ---"
                    pip install flake8
                    flake8 app.py --max-line-length=120 --ignore=E501 || true

                    echo "--- Build stage complete ---"
                '''
            }
            post {
                always {
                    echo 'Test stage complete.'
                }
                failure {
                    echo 'Tests FAILED. Stopping pipeline.'
                }
            }
        }

        // ── STAGE 3: DOCKER BUILD & PUSH ──────────────────────────────────────
        stage('Stage 3: Docker Build & Push') {
            steps {
                echo '========== Building Docker image =========='
                sh '''
                    docker build -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} \
                               ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                    echo "Docker image built: ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
                '''

                echo '========== Pushing Docker image to DockerHub =========='
                sh '''
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest
                    docker logout
                    echo "Image pushed to DockerHub successfully!"
                '''
            }
            post {
                success {
                    echo "Docker image available at: https://hub.docker.com/r/${DOCKERHUB_USERNAME}/${IMAGE_NAME}"
                }
            }
        }

        // ── STAGE 4: DEPLOY TO AWS EC2 (Nice to Have) ─────────────────────────
        stage('Stage 4: Deploy to AWS EC2') {
            when {
                branch 'main'   // Only deploy when merging to main branch
            }
            steps {
                echo '========== Deploying to AWS EC2 via SSH =========='
                sh '''
                    ssh -o StrictHostKeyChecking=no -i ${EC2_SSH_KEY} ${EC2_HOST} << 'EOF'
                        echo "Connected to EC2 instance"

                        # Pull latest Docker image
                        docker pull ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest

                        # Stop and remove existing container if running
                        docker stop smarttrack-app || true
                        docker rm smarttrack-app || true

                        # Run the new container
                        docker run -d \
                            --name smarttrack-app \
                            -p 5000:5000 \
                            --restart unless-stopped \
                            ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest

                        echo "SmartTrack deployed successfully on EC2!"
                        docker ps | grep smarttrack
EOF
                '''
            }
            post {
                success {
                    echo "Deployment to EC2 complete. App running at http://${EC2_HOST}:5000"
                }
            }
        }
    }

    // ── POST PIPELINE ─────────────────────────────────────────────────────────
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Image: docker pull ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:latest"
        }
        failure {
            echo '❌ Pipeline FAILED. Check the logs above.'
        }
        always {
            sh 'docker image prune -f || true'
            cleanWs()
        }
    }
}
