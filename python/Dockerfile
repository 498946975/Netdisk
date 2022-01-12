#基础镜像为centos，版本为7，build镜像时会自动下载
FROM centos:7

#制作者信息
MAINTAINER 498946975@qq.com

#设置环境变量
ENV CODE_DIR=/opt
ENV DOCKER_SCRIPTS=$CODE_DIR/python

#将scripts下的文件复制到镜像中的DOCKER_SCRIPTS目录
COPY ./python/* $DOCKER_SCRIPTS/

#执行镜像中的provision.sh脚本
RUN chmod a+x $DOCKER_SCRIPTS/*
RUN $DOCKER_SCRIPTS/provision.sh