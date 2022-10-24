
# SUDA-Net-Daemon

[中文README](README.md)

Daemon of Soochow University school network connection.

Download the chrome web driver from https://chromedriver.chromium.org/downloads.

## Installation
Based on the Google Chrome browser, check your chrome broswer version, then download the chrome driver from [here](https://chromedriver.chromium.org/downloads) and replace the `chromedriver.exe`.

Based on Google Chrome browser.

```sh
pip install -r requirements.txt
```

## Run
1. Edit the host for login and your account information in `configuration.json`.

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
2. Run script:

    ```sh
    python daemon.py
    ```

## Todo
1. Startup with system
2. Visualization: GUI interface + tray
3. Lightweight: remove ChromeDriver dependency