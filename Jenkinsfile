pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('🔧 Build') {
            steps {
                echo '🔧 Setting up virtual environment and installing requirements...'
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\activate && pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('🗃️ Migrate') {
            steps {
                echo 'Running Django migrations...'
                bat '%VENV_DIR%\\Scripts\\activate && python manage.py migrate'
            }
        }

        stage('✅ Unit Tests') {
            steps {
                echo 'Running unit tests...'
                bat '%VENV_DIR%\\Scripts\\activate && python manage.py test'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo 'Deployment placeholder – add real deploy logic here if needed.'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo '✅ Build completed successfully.'
        }
        failure {
            echo '❌ Build failed. Check logs.'
        }
    }
}
