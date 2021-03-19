import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

url = 'http://a.suda.edu.cn'
chrome = webdriver.Chrome(executable_path='chromedriver.exe')
chrome.get(url)

def logout():
    logout = chrome.find_element_by_name('logout')
    confirm_logout_xpath = '/html/body/div[2]/div/div[2]/form/input[1]'


def check():
    chrome.get(url)

    successed = False
    success_info_xpath = '//*[@id="edit_body"]/div/div[1]/form/div[1]'

    message_xpath = '//*[@id="message"]'
    succecc_msg = '您已经成功登录。'
    try:
        successed = (succecc_msg == chrome.find_element_by_xpath(success_info_xpath).text.strip())
    except NoSuchElementException as e:
        pass
    try:
        if successed:
            message = succecc_msg
        else:
            msg = chrome.find_element_by_xpath(message_xpath).text
            message = msg
    except Exception as e:
        message = '登录失败'
    # print(message)
    return successed, message


def login(u='', p=''):
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
    time.sleep(0.5)
    password_input.send_keys(p)
    time.sleep(0.5)
    login_bt.submit()


if __name__ == '__main__':
    file_path = 'account.json'
    with open(file_path, 'r','utf8') as f:
        obj = json.load(f)
    account = obj['account']
    password = obj['password']

    delay = 10
    print('后台运行维持网络连接。')
    msg=''
    while True:
        # time.sleep(delay)
        try:
            print(f'\r检查网络连接中。', end='')
            s, m = check()
            if not s:
                login(account, password)
            msg = m[:min(7, len(m))]
        except Exception as e:
            # print(e)
            pass
        t = delay
        for i in range(t, 0, -1):
            print(f'\r当前状态：{msg}，下一次检查：{i}s。', end='')
            time.sleep(1)
    chrome.close()
    print('\n程序终止。')
