pipeline {
    agent any 

    stages {

        stage('Setup Python') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                python --version 
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pytest
                '''
            }
        }

        stage('Train Model') {
            steps{
                bat '''
                call venv\\Scripts\\activate
                python train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps{
                bat 'docker build -t jenkins-CI-CD .'
            }
        }

        stage('Stop Old Container') {
            steps{
                bat 'docker rm -f jenkins-container-2 || exit 0'
            }
        }

        stage('Run Container') {
            steps{
                bat 'docker run -d -p 5000:5000 --name jenkins-container-2 jenkins-CI-CD'
            }
        }
    }
}   