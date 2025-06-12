pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('🔧 Setup') {
            steps {
                echo '🔧 Setting up virtual environment and installing requirements...'
                bat 'python -m venv venv'
                bat '.\\venv\\Scripts\\activate && pip install --upgrade pip'
                bat '.\\venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('🗃️ Migrate') {
            steps {
                echo 'Applying Django migrations...'
                bat '.\\venv\\Scripts\\activate && python manage.py migrate'
            }
        }

        stage('✅ Run Unit Tests') {
            steps {
                echo 'Running Django unit tests...'
                bat '.\\venv\\Scripts\\activate && python manage.py test'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo '🚧 Deployment placeholder (optional)'
            }
        }
    }

    post {
        always {
            echo '🔁 Pipeline completed.'
        }
        success {
            echo '✅ SUCCESS: All stages passed!'
        }
        failure {
            echo '❌ FAILURE: Check Console Output for errors.'
        }
    }
}
