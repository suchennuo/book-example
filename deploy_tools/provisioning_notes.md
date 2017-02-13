配置新网站
======

## 需要安装的包：

* nginx
* Python3
* Git
* pip
* virtualenv

以 Ubuntu 为例， 可以执行以下安装命令：
```
sudo apt-get install nginx python3 python3-pip
sudo pip3 install virtualenv
```
## 配置 Nginx 虚拟机
* 参考 nginx.template.conf
* 把 SITENAME 替换成所需的域名，例如 yongchaozhang.com

## Upstart 任务
* 参考 gunicorn-upstart.temlate.conf
* 把 SITENAME 替换成所需要的域名

## 文件夹结构：
假设有用户账户，home 目录为 home/username
```
/home/username
|___sites
    |___SITENAME
        |___database
        |___source
        |___static
        |___virtualenv
```