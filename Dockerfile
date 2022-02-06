#基于的基础镜像
FROM harbor.liuxiang.com/python/python:3.7

#语言编码设置
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LC_ALL zh_CN.UTF-8

#设置工作目录
WORKDIR /code

#拷贝安装文件到/code目录下
COPY requirements.txt /code

#安装虚拟环境
RUN pip3 install --upgrade pip \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip3 install -r requirements.txt

#拷贝当前目录下的所有文件到工作目录
COPY . /code/