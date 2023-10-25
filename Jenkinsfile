pipeline {
    agent { 
        node {
            label 'docker-agent-ewauf'
            }
      }
    triggers {
        pollSCM '* * * * *'
    }

    stages {
        stage('Check Dependencies/Requirements') {
            steps {
                echo "Checking Dependencies..."
                sh '''
                cd Ewauf
                pip3 install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing..."
                sh '''
                cd Ewauf
                python3 Ewauf_Run.py
                '''
            }
        }
        stage('Get Logs') {
            steps {
                echo "Getting Logs..."
                sh '''
                cd Ewauf
                log_file=$(ls logs | grep '\\.log$')
                cd logs
                cat $log_file
                '''
            }
        }
    }
}
