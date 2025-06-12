pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('🔧 Build Environment') {
            steps {
                echo '📦 Creating virtual environment and installing dependencies...'
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\activate && pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('🗃️ Apply Migrations') {
            steps {
                echo '⚙️ Running Django migrations...'
                bat '%VENV_DIR%\\Scripts\\activate && python manage.py migrate'
            }
        }

        stage('✅ Run Unit Tests') {
            steps {
                echo '🧪 Running Django unit tests...'
                bat '%VENV_DIR%\\Scripts\\activate && python manage.py test'
            }
        }

        stage('🚀 Deploy (placeholder)') {
            steps {
                echo '🚧 Deployment stage - add deployment logic here if needed.'
            }
        }
    }

    post {
        always {
            echo '🔁 Pipeline execution completed.'
        }
        success {
            echo '✅ SUCCESS: All steps completed successfully!'
        }
        failure {
            echo '❌ FAILURE: Errors encountered during pipeline.'
        }
    }
}
