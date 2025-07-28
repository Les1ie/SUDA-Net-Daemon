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
    # ==================== 新增代码开始 ====================
    try:

        dropdown_xpath = '//*[@id="edit_body"]/div[2]/div[12]/select'
        chrome.find_element_by_xpath(dropdown_xpath).click()

        time.sleep(1)


        operator_xpath = '//*[@id="edit_body"]/div[2]/div[12]/select/option[3]'
        chrome.find_element_by_xpath(operator_xpath).click()
        
        time.sleep(1)
        
    except Exception as e:
        logger.error('选择运营商时出错！请检查下拉菜单的XPath是否正确。', exc_info=True)
        return # 直接退出login函数

    # ==================== 新增代码结束 ====================
	
    account_input_xpath = '//*[@id="edit_body"]/div[2]/div[12]/form/input[3]'
    password_input_xpath = '//*[@id="edit_body"]/div[2]/div[12]/form/input[4]'
    login_bt_xpath = '//*[@id="edit_body"]/div[2]/div[12]/form/input[2]'

    account_input = chrome.find_element_by_xpath(account_input_xpath)
    password_input = chrome.find_element_by_xpath(password_input_xpath)
    login_bt = chrome.find_element_by_xpath(login_bt_xpath)
    
    account_input.click()      
    time.sleep(0.5)            
    account_input.clear()
    account_input.send_keys(u)
    
    password_input.click()     
    time.sleep(0.5)            
    password_input.clear()
    password_input.send_keys(p)
        # 执行脚本生成隐藏的随机验证码，并登录
    chrome.execute_script('arguments[0].click()', login_bt)
    # ActionChains(driver=chrome).move_to_element(login_bt).click(login_bt)
    # login_bt.click()


def init_chrome(host):
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    # chrome_options.add_argument('--headless')  # 无头模式
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
    user_cfg_path = 'configuration.json'
    user_config = None
    
    try:
        with open(user_cfg_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
    except FileNotFoundError:
        logger.error(f"错误：配置文件 '{user_cfg_path}' 不存在，请检查文件名和路径。")
        exit() # 文件不存在，程序无法继续
    except json.JSONDecodeError:
        logger.error(f"错误：配置文件 '{user_cfg_path}' 格式不正确，请检查是否为标准JSON。")
        exit() # JSON格式错误，程序无法继续
    except Exception as e:
        logger.error(f"读取配置文件时发生未知错误: {e}")
        exit()
    
    try:
        host = user_config['daemon']['host']
        account = user_config['login']['account']
        password = user_config['login']['password']
        delay = user_config['daemon']['frequencies']
    except KeyError as e:
        logger.error(f"错误：配置文件中缺少必要的键（Key）：{e}。请检查配置文件结构。")
        exit()

    logger.info("正在初始化浏览器...")
    chrome = init_chrome(host)
    if not chrome:
        logger.error("浏览器初始化失败，程序退出。")
        exit()

    logger.info("初始化完成，开始后台监控网络连接...")
       
    while True:
        try:            
            s, m = check(chrome, host)
            dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            if not s:                
                print(f'\n[{dt}] 状态：{m} 尝试登录...')
                login(chrome, account, password)
                time.sleep(3) # 登录后等待3秒让页面稳定
                # 再次检查状态以确认登录结果
                s, m = check(chrome, host)
                dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
           
            if s:
                msg = f"已成功登录。[{dt}]"
            else:
                msg = f"尝试登录后仍未登录。[{dt}]"
                        
            for i in range(delay, 0, -1):
                print(f'\r{msg} 下次检查还剩: {i}秒', end='')
                time.sleep(1)

        except Exception as e:
            logger.error(f'\n主循环发生严重错误: {e}', exc_info=True)
            logger.info("程序将在30秒后尝试恢复...")
            time.sleep(30)