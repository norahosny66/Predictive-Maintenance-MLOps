pipeline {
    agent any

    options {
        skipDefaultCheckout()  // Disable Jenkins auto-clone
    }

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout (Skip Large Folders)') {
            steps {
                script {
                    sh '''
                    rm -rf repo && mkdir repo && cd repo

                    git init
                    git remote add origin git@github.com:norahosny66/Predictive-Maintenance-MLOps.git
                    
                    # Enable sparse checkout to avoid downloading heavy folders
                    git config core.sparseCheckout true
                    echo "/*" > .git/info/sparse-checkout
                    echo "!/dataset/" >> .git/info/sparse-checkout
                    echo "!/venv/" >> .git/info/sparse-checkout
                    echo "!/mlruns/" >> .git/info/sparse-checkout
                    # Fetch only the latest commit
                    git pull --depth=1 origin main
                    '''
                }
            }
        }

        stage('Setup Virtual Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r repo/requirements.txt
                '''
            }
        }

        
    }
}
