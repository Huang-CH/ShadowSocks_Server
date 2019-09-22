#!/usr/bin/env python
#coding:utf-8

import os
import time

def install_pip():
    '''
    这是一个CentOS 7安装pip的函数
    :return:
    '''
    #更新系统
    yum_update=os.system('yum -y update')
    if yum_update == 0:
        print('<!--- 系统更新成功 ---!>')
        time.sleep(1)
    else:
        print('<!--- 系统更新失败 ---!>')
        time.sleep(1)

    #安装epel扩展源
    yum_epel=os.system('yum -y install epel-release')
    if yum_epel == 0:
        print('<!--- epel扩展源安装成功 ---!>')
        time.sleep(1)
    else:
        print('<!--- epel扩展源安装失败 ---!>')
        time.sleep(1)

    #安装pip
    yum_pip=os.system('yum -y install python-pip')
    if yum_pip == 0:
        print('<!--- pip安装成功 ---!>')
        time.sleep(1)
    else:
        print('<!--- pip安装失败 ---!>')
        time.sleep(1)

    #清除cache
    yum_clean_all=os.system('yum clean all')
    if yum_clean_all == 0:
        print('<!--- 清除cache成功 ---!>')
        time.sleep(1)
    else:
        print('<!--- 清除cache失败 ---!>')
        time.sleep(1)

    #升级pip到最新版本
    pip_upgrade=os.system('pip install --upgrade pip')
    if pip_upgrade == 0:
        print('<!--- 升级pip成功 ---!>')
        time.sleep(1)
    else:
        print('<!--- 升级pip失败 ---!>')
        time.sleep(1)

def install_shadowsocks():
    '''
    这是一个安装shadowsocks的函数
    :return:
    '''
    #pip安装python版本的shadowsocks
    os.system('pip install shadowsocks')

def configuration_shadowsocks():
    '''
    这是一个配置shadowsocks的函数
    :return:
    '''
    #编辑shadowsocks.json配置文件
    with open(r'/etc/shadowsocks.json',mode='w',encoding='utf-8') as f:
        f.write('''
    {
    "server": “0.0.0.0",
    "server_port": %s,
    "password": %s,
    "method": “aes-256-cfb"
    }
    ''' %(server_port,user_password))

    #生成配置log
    with open(r'/etc/shadowsocks.json',mode='rb') as src_file,open(r'~/shadowsocks.log',mode='wb') as dis_file:
        for line in src_file:
            dis_file.write(line)

def configuration_self_startup():
    '''
    这是一个配置shadowssocks自启动的函数
    :return:
    '''
    #编辑启动脚本
    with open(r'/etc/systemd/system/shadowsocks.service',mode='w',encoding='utf-8') as f:
        f.write('''
    [Unit]
    Description=Shadowsocks
    
    [Service]
    TimeoutStartSec=0
    ExecStart=/usr/bin/ssserver -c /etc/shadowsocks.json
    
    [Install]
    WantedBy=multi-user.target    
    ''')

    #启动shadowsocks服务
    os.system('systemctl enable shadowsocks')
    os.system('systemctl start shadowsocks')

def receiving_service_port():
    '''
    这是一个接收用户输入端口号的函数
    :return: server_port
    '''
    while 1:
        print('=' * 50)
        server_port = input('请输入端口号（1025至65535任选一个）：').strip()
        if server_port.isdigit():
            return server_port
            break
        else:
            print('<!--- 端口号只能填写数字 ---!>')

def receiving_user_password():
    '''
    这是一个接收用户密码的函数
    :return:user_password
    '''
    while 1:
        print('=' * 50)
        user_password=input('请输入您的密码：').strip()
        print('=' * 50)
        user_password_confirm=input('<!--- 您输入的密码为：%s ---!> 确认无误请输入“Y”,重新输入请安任意键:' %(user_password)).strip()
        print('=' * 50)
        if user_password_confirm == 'Y' or user_password_confirm == 'y':
            return user_password
            break

def configure_firewall():
    os.system('firewall-cmd --zone=public --add-port={}/tcp --permanent'.format(server_port))
    os.system('firewall-cmd --reload')

if __name__ == '__main__':
    install_pip()
    install_shadowsocks()
    server_port = receiving_service_port()
    user_password = receiving_user_password()
    configuration_shadowsocks()
    configuration_self_startup()
    configure_firewall()



