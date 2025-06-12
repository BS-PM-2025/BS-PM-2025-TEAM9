pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Build') {
            steps {
                echo '🔧 Creating virtual environment and installing dependencies...'
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate && pip install --upgrade pip'
                bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo '✅ Running Django tests...'
                bat '.\\venv\\Scripts\\activate && python manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Simulated deploy step (can add real commands here)'
            }
        }
    }

    post {
        always {
            echo '🔁 Pipeline finished.'
        }
        success {
            echo '✅ SUCCESS!'
        }
        failure {
            echo '❌ FAILURE – check Console Output.'
        }
    }
}
