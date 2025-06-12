pipeline {
    agent any

    stages {
        stage('🔧 Install Requirements') {
            steps {
                echo '📦 Installing requirements...'
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

        stage('✅ Run Unit Tests') {
            steps {
                echo '✅ Running tests...'
                sh 'python3 manage.py test'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo '🚀 Deployment placeholder'
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
