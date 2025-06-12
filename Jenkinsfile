pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('🔧 Setup Environment') {
            steps {
                echo '📦 Creating virtual environment and installing requirements...'
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\activate && pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('🗃️ Apply Migrations') {
            steps {
                echo '⚙️ Applying Django migrations...'
                bat """
                call %VENV_DIR%\\Scripts\\activate
                python manage.py migrate
                """
            }
        }

        stage('✅ Run Unit Tests') {
            steps {
                echo '🧪 Running Django unit tests...'
                bat """
                call %VENV_DIR%\\Scripts\\activate
                python manage.py test
                """
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
            echo '🔁 Jenkins Pipeline completed.'
        }
        success {
            echo '✅ SUCCESS: All stages passed!'
        }
        failure {
            echo '❌ FAILURE: Check Console Output for errors.'
        }
    }
}
