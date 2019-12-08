# -*- coding:utf-8 -*-
# author:Changing Xu
# file:Crawler_tudinet-AgainCrawler
# datetime:2019/12/7 14:05
# software: PyCharm
import requests
import http.cookiejar as cj
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt
from PIL import Image
import os


def againCrawlerJudge(res):
    '''
    利用encoding和apparent_encoding判断是否为反爬虫页面
    :param res:
    :return:
    '''
    if res.encoding != res.apparent_encoding:
        return False
    else:
        return res.text.encode(res.apparent_encoding)


def againCrawlerWebdrive(url):
    chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    driver.set_window_size(1200, 800)
    cookies = driver.get_cookies()
    driver.implicitly_wait(2)
    driver.get(url)
    # 获取截图
    driver.get_screenshot_as_file('tmp/screenshot.png')
    # 获取元素指定位置
    element = driver.find_element_by_class_name('yz')
    left = int(element.location['x'])
    top = int(element.location['y'])
    right = int(element.location['x'] + element.size['width'])
    bottom = int(element.location['y'] + element.size['height'])
    # 通过Image处理图像
    im = Image.open('tmp/screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('tmp/code.png')
    plt.imshow(im)
    plt.show()
    # 输入和登陆按钮确定
    verification_code_input = driver.find_element_by_class_name("inp_s")
    confirm_button = driver.find_element_by_class_name("btn")
    verification_code_input.send_keys(input('验证码：'))
    confirm_button.click()
    time.sleep(10)
    page_source = driver.page_source
    cookies = driver.get_cookies()
    driver.close()
    return page_source, cookies


def againCrawlerWebdriveTest(url):
    chromedriver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    driver.set_window_size(1200, 800)
    cookies = driver.get_cookies()
    # 处理cookies
    driver.implicitly_wait(2)
    driver.get(url)
    print(driver.page_source)
    cookies = driver.get_cookies()
    print(cookies)
    driver.close()


# url = 'https://www.tudinet.com/market-84-0-0-0/list-pg2.html'
# session = loadSessionCookie(requests.Session())
# list_pg_get = session.get(url, **getSessionPara(url))
# print(list_pg_get.encoding)  # 查看网页返回的字符集类型
# print(list_pg_get.apparent_encoding)  # 自动判断字符集类型
# list_pg_get.encoding = list_pg_get.apparent_encoding
# html = list_pg_get.text
# print(html)
# againCrawlerWebdriveTest('https://www.tudinet.com/market-84-0-0-0/list-pg2.html')
