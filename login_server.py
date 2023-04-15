#!/usr/bin/python
# -*- coding: utf-8 -*-
# pip install selenium
# pip install Image
# pip install baidu-aip
import os
import shutil
import sys
import re
import time
import baidu_ocr
from selenium import webdriver
from PIL import Image
from selenium.webdriver.chrome.options import Options
import logging
import datetime

USER_NAME = sys.argv[1]
PASSWORD = sys.argv[2]

# 设置日志级别和格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
# 获取当前日期
now = datetime.datetime.now()
date = now.strftime('%Y-%m-%d')

# 创建日志文件名并创建对应的Handler
log_file = f"./log/log_{date}.log"
file_handler = logging.FileHandler(log_file)

# 设置Handler级别和格式
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

# 添加 Handler 到 logger 对象中
logging.getLogger('').addHandler(file_handler)


def code_process():
    # 登录页面截图
    browser.save_screenshot(loginImage)
    logging.info(USER_NAME + "截图完成")
    # 获取图片验证码坐标
    code_ele = browser.find_element("xpath", '//*[@id="imgCode"]')
    # 图片4个点的坐标位置
    left = code_ele.location['x'] + 310  # x点的坐标
    top = code_ele.location['y'] + 25  # y点的坐标
    right = code_ele.size['width'] + left + 30  # 上面右边点的坐标
    down = code_ele.size['height'] + top + 50  # 下面右边点的坐标
    image = Image.open(loginImage)
    # 将图片验证码截取
    code_image = image.crop((left, top, right, down))
    code_image.save(codeImage)  # 截取的验证码图片保存为新的文件

    image = Image.open(codeImage)

    width, height = image.size
    segment_size = height // 2
    lower_segment = image.crop((0, segment_size, width, height))
    lower_segment.save(codeImage)

    image = Image.open(codeImage)
    img = image.convert('L')  # P模式转换为L模式(灰度模式默认阈值127)
    count = 130  # 设定阈值
    table = []
    for m in range(256):
        if m < count:
            table.append(0)
        else:
            table.append(1)
    img = img.point(table, '1')
    img.save(path + "/code1.png")  # 保存处理后的验证码


def img_check(i=0):
    logging.info(USER_NAME + "开始识别验证码")
    # 调用百度云接口
    api = baidu_ocr.word(codeImage)
    results = api.General()

    for result in results["words_result"]:
        text = result["words"]
        text = text.strip()
        # 替换特殊字符 re.match("^[a-zA-Z0-9]*$", text)
        text = re.sub(r'[^A-Za-z0-9]+', '', text)
        if len(text) == 4:
            logging.info("格式正确" + str(i) + ": "+text)
            time.sleep(1)
            browser.find_element("xpath", '//*[@id="usernamepsw"]').clear()
            time.sleep(1)
            browser.find_element(
                "xpath", '//*[@id="usernamepsw"]').send_keys(USER_NAME)
            browser.find_element(
                "xpath", '//*[@id="password"]').send_keys(PASSWORD)
            browser.find_element(
                "xpath", '//*[@id="fm1"]/ul/li[3]/input').send_keys(text)

            # 提交按钮查看按钮元素，click模拟点击提交
            browser.find_element(
                "xpath", '//*[@id="fm1"]/ul/li[5]/button').click()
            browser.implicitly_wait(10)
            if "https://sso.cuit.edu.cn/authserver/login" not in browser.current_url:
                logging.info("第" + str(i) + "次尝试登录成功")
                return
            else:
                i += 1
                logging.warning("第" + str(i) + "次尝试登录失败，正在重试")
                code_process()
                img_check(i)

        else:
            browser.refresh()
            logging.warning("第" + str(i) + "次图片识别失败")
            if i > 20:
                logging.error('重试次数过多，验证码获取失败，请稍后重试')
                browser.quit()
                sys.exit(0)
            else:
                i += 1
                code_process()
                img_check(i)


if __name__ == '__main__':
    i = 0
    path = os.path.abspath(os.path.dirname(__file__))
    loginImage = path + "/login.png"  # 登录页面截图
    codeImage = path + "/code.png"  # 定位验证码截图

    chrome_options = Options()

    chrome_options.add_argument('--lang=zh-CN')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--font-rendering-engine=skia')
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.maximize_window()

    # 登录校外VPN
    j = 0
    while True:
        url = 'https://webvpn.cuit.edu.cn/portal/?redirect_uri=http%3A%2F%2Fjwgl-cuit-edu-cn.webvpn.cuit.edu.cn%3A8118%2Feams%2Fhome.action#!/login'
        browser.get(url)
        browser.implicitly_wait(10)

        if j == 0:
            browser.find_element(
                "xpath", '//*[@id="Calc"]/div[3]/span/div[1]').click()
        time.sleep(1)
        browser.find_element(
            "xpath", '//*[@id="loginPwd"]').send_keys(PASSWORD)
        browser.find_element(
            "xpath", '/html/body/div[2]/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/div[1]/div/div[1]/input').send_keys(USER_NAME)

        browser.find_element("xpath", '//*[@id="Calc"]/div[4]/button').click()
        j += 1
        # 登录统一身份验证

        browser.implicitly_wait(10)
        try:
            username = browser.find_element("xpath", '//*[@id="usernamepsw"]')
            break
        except:
            continue

    logging.info(USER_NAME + "进入统一登录页面")
    username.clear()
    username.send_keys(USER_NAME)
    username.clear()
    username.send_keys(USER_NAME)

    # 读取验证码
    code_process()
    # 绕过验证码完成登录
    img_check(i)
    browser.implicitly_wait(10)

    # 进入教务处课表页面
    browser.find_element(
        "xpath", '//*[@id="menu_panel"]/ul/li[1]/ul/div/li[4]/a').click()
    time.sleep(1)

    js_file_path = path + "/capture_json_data.js"
    with open(js_file_path, "r") as file:
        js_code = file.read()
    try:
        browser.execute_script(js_code)
    except:
        logging.error("javascript execution failed")
    time.sleep(1)
    browser.quit()
    # 指定源文件路径
    source_file = "/home/root/Downloads/"

    # 指定目标文件夹路径
    os.system("mkdir -p /root/cuit_agent/py/" + USER_NAME)
    target_folder = "/root/cuit_agent/py/" + USER_NAME

    # 使用shutil库中的move()函数移动文件
    files = os.listdir(source_file)
    for file in files:
        if "学期" in file and ".json" in file:
            try:
                shutil.move(source_file + file, target_folder)

            except:
                logging.error(f"file {file} already exists")
            break
    logging.info("END")
