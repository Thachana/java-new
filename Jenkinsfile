pipeline {
    agent any

    environment {
        DOCKER_HUB = 'thachana/my-crud-app'
        SONARQUBE = 'sonar'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Thachana/crud-jenkins-pipeline.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonar') {
                    sh 'sonar-scanner -Dsonar.projectKey=crud-jenkins -Dsonar.sources=.'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_HUB:latest ./app'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL $DOCKER_HUB:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $DOCKER_HUB:latest'
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                sh 'docker compose down && docker compose up -d'
            }
        }
    }
}
