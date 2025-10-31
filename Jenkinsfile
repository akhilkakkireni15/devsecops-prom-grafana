pipeline {
  agent {
    label 'vish-security-agent'
  }
  environment {
    APP_NAME = "flask-counter"
  }
  stages {
    stage('Build Docker Image') {
      steps {
        sh '''
          cd app
          docker build -t ${APP_NAME}:latest .
        '''
      }
    }
    stage('Run Monitoring Stack') {
      steps {
        sh '''
          docker compose -f docker-compose.yml up -d
          sleep 10
        '''
      }
    }
    stage('Run App Container') {
      steps {
        sh '''
          docker run -d --name ${APP_NAME} --network monitoring-lab_monitoring             -p 5000:5000 ${APP_NAME}:latest
        '''
      }
    }
    stage('Validate Metrics') {
      steps {
        sh '''
          echo "Prometheus Targets:"
          curl -s http://34.228.140.38:8006/api/v1/targets | jq '.data.activeTargets'
        '''
      }
    }
    stage('Health Check') {
      steps {
        script {
          def resp = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5000", returnStdout: true).trim()
          if (resp != '200') {
            error "Application failed health check!"
          } else {
            echo "App is healthy ✅"
          }
        }
      }
    }
  }
  post {
    always {
      sh 'docker ps'
    }
  }
}