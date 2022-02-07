node('jenkins-test') {
    stage('Change hosts') {
        echo "1.Change hosts files"
        sh 'echo "172.16.120.55 gitlab.liuxiang.com" >> /etc/hosts'
        sh 'echo "172.16.120.44 harbor.liuxiang.com" >> /etc/hosts'
    }
    stage('Clone') {
        echo "2.Clone Stage"
        git branch: 'master', url: 'http://gitlab.liuxiang.com:13800/liuxiang/netdisk.git'
        script {
            build_tag = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
        }
    }
    stage('Build') {
        echo "3.Build Docker Image Stage"
        sh "docker build -t registry.cn-hangzhou.aliyuncs.com/876500/netdisk:${build_tag} ."
    }
    stage('Push') {
        echo "4.Push Docker Image Stage"
        withCredentials([usernamePassword(credentialsId: 'login_aliyun', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
            sh "docker login -u ${dockerHubUser} -p ${dockerHubPassword} registry.cn-hangzhou.aliyuncs.com"
            sh "docker push registry.cn-hangzhou.aliyuncs.com/876500/netdisk:${build_tag}"
        }
    }
    stage('Promote to develop') {
        def userInput = input(
            id: 'userInput',
            message: 'Promote to develop?',
            parameters: [
                [
                    $class: 'ChoiceParameterDefinition',
                    choices: "YES\nNO",
                    name: 'Env'
                ]
            ]
        )
        echo "This is a deploy step to ${userInput}"
        if (userInput == "YES") {
            sh "sed -i 's/<BUILD_TAG>/${build_tag}/' ./deploy/develop.yaml"
            sh "sed -i 's/<BRANCH_NAME>/${env.BRANCH_NAME}/' ./deploy/develop.yaml"
            sh "kubectl apply -f ./deploy/develop.yaml --validate=false"
            sh "kubectl apply -f ./deploy/develop_ingress.yaml --validate=false"
            sh "kubectl get pods -n develop"
        } else {
            //exit
        }
    }
    stage('Promote to production') {
        def userInput = input(
            id: 'userInput',
            message: 'Promote to production?',
            parameters: [
                [
                    $class: 'ChoiceParameterDefinition',
                    choices: "YES\nNO",
                    name: 'Env'
                ]
            ]
        )
        echo "This is a deploy step to ${userInput}"
        if (userInput == "YES") {
            sh "sed -i 's/<BUILD_TAG>/${build_tag}/' ./develop/production.yaml"
            sh "sed -i 's/<BRANCH_NAME>/${env.BRANCH_NAME}/' ./develop/production.yaml"
            sh "kubectl apply -f ./develop/production.yaml --record --validate=false"
            sh "kubectl apply -f ./develop/production_ingress.yaml --record --validate=false"
            sh "kubectl get pods -n production"
        }
    }
}