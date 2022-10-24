# 苏州大学校园网守护进程

[英文README](README.en.md)

苏州大学校园网守护进程，妈妈再也不用担心<del>老子</del>实验室电脑断网了！

主要适用于无人值守的环境下确保某台设备网络稳定（请确保校园网账户余额充足）：
- 多设备连接时，超过3台设备会挤掉其他设备；
- 每月第一天00:00左右自动断网。

主要运行流程：
1. 判定登录状态：检查登录页面是否存在登陆状态关键字、账号信息输入输入框以判定当前登录状态
2. 尝试登陆：未登录则尝试登录
3. 休眠指定时间，并进入`1.`，无限循环
4. 结束运行：手动停止运行或被操作系统终止

## 使用
使用方式有两种：
- 发行版，无 Python 环境依赖，直接运行 `.exe` 文件；
- 源码，本地 Python 命令运行。

### 运行发行版

[下载发行版](https://github.com/Les1ie/SUDA-Net-Daemon/releases)，并按照说明运行。

### 运行源码
#### 安装

基于 Python 开发，要求使用 Chrome 浏览器驱动（[下载地址](https://chromedriver.chromium.org/downloads)），**下载和本地 Chorme 浏览器对应版本的驱动**后替换 `chromedriver.exe`。

安装 Python 依赖：

```sh
pip install -r requirements.txt
```

#### 运行
1. 在 `configurations.json` 中编辑校园网登录IP、账号密码等配置信息，默认配置格式如下：

    ```json
    {
        "login":{
            "account":"",
            "password":""
        },
        "daemon":{
                "host": "http://10.9.1.3/",
                "frequencies": 10
        }
    }
    ```

2. 运行如下命令:

    ```sh
    python daemon.py
    ```

## Todo
1. 开机启动
2. 可视化：GUI界面+托盘
3. 轻量化：去除 ChromeDriver 依赖

