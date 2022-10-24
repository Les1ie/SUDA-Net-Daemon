import time
import json
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException

logger = logging.getLogger('SUDA-Net-Daemon')
logger.setLevel('ERROR')
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s', '%d/%m/%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


def logout(chrome):
    logout = chrome.find_element_by_name('logout')
    confirm_logout_xpath = '/html/body/div[2]/div/div[2]/form/input[1]'


def check(chrome, host):
    chrome.get(host)

    successed = False
    success_info_xpath = '//*[@id="edit_body"]/div/div[1]/form/div[1]'

    message_xpath = '//*[@id="message"]'
    succecc_msg = '您已经成功登录。'
    try:
        successed = (succecc_msg == chrome.find_element_by_xpath(
            success_info_xpath).text.strip())
    except NoSuchElementException as e:
        # logger.error('未找到检测目标', exc_info=True)
        pass

    if successed:
        message = succecc_msg
    else:
        try:
            msg = chrome.find_element_by_xpath(message_xpath).text
            message = msg
        except NoSuchElementException as e:
            # 未登录
            message = '未登录，尝试登录。'
        except Exception as e:
            message = '页面状态解析失败。'
            logger.error(message, exc_info=True)
    # print(message)
    return successed, message


def login(chrome, u='', p=''):
    # 选择'普通登录'
    # chrome.find_element_by_xpath('//*[@id="edit_body"]/div[1]/div[3]/div/div[1]/span[1]').click()

    account_input_xpath = '//*[@id="edit_body"]/div[2]/div[4]/div/div[2]/div[1]/div/form/input[3]'
    password_input_xpath = '//*[@id="edit_body"]/div[2]/div[4]/div/div[2]/div[1]/div/form/input[4]'
    login_bt_xpath = '//*[@id="edit_body"]/div[2]/div[4]/div/div[2]/div[1]/div/form/input[2]'

    account_input = chrome.find_element_by_xpath(account_input_xpath)
    password_input = chrome.find_element_by_xpath(password_input_xpath)
    login_bt = chrome.find_element_by_xpath(login_bt_xpath)
    account_input.clear()
    password_input.clear()
    account_input.send_keys(u)
    password_input.send_keys(p)
    # 执行脚本生成隐藏的随机验证码，并登录
    chrome.execute_script('arguments[0].click()', login_bt)
    # ActionChains(driver=chrome).move_to_element(login_bt).click(login_bt)
    # login_bt.click()


def init_chrome(host):
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 不弹出界面
    chrome_options.add_argument('--incognito')  # 无痕隐身模式
    chrome_options.add_argument("disable-cache")    # 禁用缓存
    chrome_options.add_argument('log-level=3')  # 过滤浏览器驱动的命令行输出

    try:
        chrome = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        chrome.get(host)
        return chrome
    except SessionNotCreatedException as e:
        logger.error(
            f'ChromeDriver 与 Chrome 版本不一致，请从 https://chromedriver.chromium.org/downloads 下载对应版本。',
            exc_info=True)
        exit()
    except Exception as e:
        logger.error(f'ChromeDriver 初始化错误', exc_info=True)
        exit()


if __name__ == '__main__':
    user_cfg_path = 'configurations.json'
    user_config = None
    try:
        with open(user_cfg_path, 'r', encoding='utf8') as f:
            user_config = json.load(f)
    except FileNotFoundError as e:
        # print('配置文件 configuration.json 不存在。')
        logger.error('配置文件 configuration.json 不存在。')
        exit()

    host = user_config['daemon']['host']
    chrome = init_chrome(host)

    account = user_config['login']['account']
    password = user_config['login']['password']

    delay = user_config['daemon']['frequencies']
    # print('后台运行维持网络连接。')
    logger.info('后台运行维持网络连接。')
    msg = ''
    dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    while True:
        # time.sleep(delay)
        try:
            print(f'\r检查网络连接中。', end='')
            s, m = check(chrome, host)
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if not s:
                login(chrome, account, password)
            msg = m[:min(7, len(m))]
        except Exception as e:
            logger.error(f'登录或状态检查出错。', exc_info=True)
        t = delay
        for i in range(t, 0, -1):
            print(f'\r当前状态：{msg} [{dt}]，下一次检查：{i}s', end='')
            time.sleep(1)
    chrome.close()

    logger.info('\n程序终止。')
