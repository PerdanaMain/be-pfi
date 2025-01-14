pipeline {
    agent any
    
    environment {
        // Replace with your Docker Hub username/organization
        DOCKER_HUB_USERNAME = 'aimodocker'
        // Use credentials for Docker Hub
        DOCKER_CREDENTIALS = credentials('aimodocker')
        // Replace with your image name
        IMAGE_NAME = 'pfi-service'
        // Replace with your docker compose service name
        SERVICE_NAME = 'oh-app'
        // Variable for Git commit hash
        GIT_COMMIT_HASH = ''

        // Replace with the SSH credentials for development server
        // SSH_CREDENTIALS = credentials('backend-server-digitaltwin')
        // SSH_CREDENTIALS_USR = 'aimo'
        // SSH_SERVER_IP = '192.168.1.82'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Checkout and get git commit hash
                    checkout scm
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    GIT_COMMIT_HASH = commitHash
                    echo "Git commit hash: ${GIT_COMMIT_HASH}"
                }
            }
        }
        
        stage('Docker Login') {
            steps {
                sh '''
                    echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build with commit hash tag
                    sh """
                        docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest .
                        docker tag ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${GIT_COMMIT_HASH}
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh """
                    # Push both tags
                    docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${GIT_COMMIT_HASH}
                    docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest
                """
            }
        }
        
        // stage('Deploy') {
        //     steps {
        //         script {
        //             sshagent(credentials: [SSH_CREDENTIALS]) {
        //                 sh """
        //                     ssh -o StrictHostKeyChecking=no ${SSH_CREDENTIALS_USR}@${SSH_SERVER_IP} '
        //                         cd ~/digital-twin/Docker
        //                         sudo docker compose pull ${SERVICE_NAME}
        //                         sudo docker compose up -d ${SERVICE_NAME}
        //                     '
        //                 """
        //             }
        //         }
        //     }
        // }
    }
    
    post {
        always {
            // Clean up
            sh 'docker logout'
            
            // Clean up local images
            script {
                try {
                    sh """
                        # Push both tags
                        docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${GIT_COMMIT_HASH}
                        docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest
                    """
                } catch (err) {
                    echo "Failed to clean up images: ${err}"
                }
            }
        }
        success {
            echo "Successfully built, pushed, and deployed Docker image with tags: latest and ${GIT_COMMIT_HASH}"
        }
        failure {
            echo 'Failed to build/push/deploy Docker image!'
        }
    }
}