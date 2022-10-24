# 苏州大学校园网守护进程

[英文README](README.en.md)

苏州大学校园网守护进程，妈妈再也不用担心实验室电脑断网了。（请确保校园网账户余额充足）

## 安装

基于 Python 开发，要求使用 Chrome 浏览器驱动（[下载地址](https://chromedriver.chromium.org/downloads)），**下载和本地 Chorme 浏览器对应版本的驱动**后替换 `chromedriver.exe`。

安装 Python 依赖：

```sh
pip install -r requirements.txt
```

## 运行
1. 在 `configuration.json` 中编辑校园网登录IP、账号密码等配置信息；
2. 运行如下命令:

```sh
python daemon.py
```

## Todo
1. 开机启动
2. 可视化：GUI界面+托盘
3. 轻量化：去除 ChromeDriver 依赖

