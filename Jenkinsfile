node('jenkins-test') {
    stage('Change hosts') {
        echo "1.Change hosts files"
        sh 'echo "172.16.120.55 gitlab.liuxiang.com" >> /etc/hosts'
        sh 'echo "172.16.120.202 harbor.liuxiang.com" >> /etc/hosts'
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
}