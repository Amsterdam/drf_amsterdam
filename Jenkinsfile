#!groovy

def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block();
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'

        throw t;
    }
    finally {
        if (tearDown) {
            tearDown();
        }
    }
}


node {
    stage("Checkout, build and run tests (do not push image).") {
        checkout scm
    }

    stage('Test') {
        tryStep "test", {
            sh "docker build -t drf_amsterdam_test . &&" +
		"docker run --rm drf_amsterdam_test python runtests.py &&" +
		"docker rmi drf_amsterdam_test"
        }
    }
}
