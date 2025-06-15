pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {
        stage('📥 Checkout Source') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
            }
        }

        stage('📦 Install Requirements') {
            steps {
                echo '📦 Installing dependencies...'
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('🗃️ Apply Migrations') {
            steps {
                echo '🗃️ Running Django migrations...'
                sh 'python3 manage.py migrate'
            }
        }

        stage('🧪 Run Unit Tests') {
            steps {
                echo '🧪 Running tests...'
                sh 'python3 manage.py test --verbosity=2'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo '🚀 Deployment step (placeholder)'
                // תוכל להוסיף כאן שליחת קבצים, docker deploy וכו'
            }
        }
    }

    post {
        always {
            echo '🔁 Pipeline finished running.'
        }
        success {
            echo '✅ All stages passed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for more info.'
        }
    }
}
