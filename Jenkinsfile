pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('🔧 Setup Environment') {
            steps {
                echo '📦 Creating virtual environment and installing requirements...'
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install --upgrade pip'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('🗃️ Apply Migrations') {
            steps {
                echo '📄 Applying Django migrations...'
                sh 'source venv/bin/activate && python manage.py migrate'
            }
        }

        stage('✅ Run Unit Tests') {
            steps {
                echo '🧪 Running Django unit tests...'
                sh 'source venv/bin/activate && python manage.py test'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo '🚀 Deploy step - placeholder'
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
