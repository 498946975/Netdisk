#!/bin/bash
set -e


#python的一些依赖
yum -y groupinstall "Development tools"
yum install -y openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel psmisc libffi-devel wget

#python3.7
wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
tar -zxvf Python-3.7.7.tgz
cd Python-3.7.7
./configure
make && make install
rm -rf Python-3.7.7

#pip3
pip3 install --upgrade pip