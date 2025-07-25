pipeline {
    agent any

    environment {
        PYTHON = 'python3'
    }

    stages {
        stage('Setup Virtual Env') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install --cache-dir=$WORKSPACE/.pip-cache -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                . venv/bin/activate
                pip install flake8 black
                flake8 src/ || true
                black --check src/ || true
                '''
            }
        }

        
    }

 
}
