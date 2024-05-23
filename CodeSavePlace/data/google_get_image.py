from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
import requests
from lxml import etree

def collect():
    option = ChromeOptions()
    #用于禁用浏览器中的自动化检测
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    # 设置中文
    option.add_argument('lang=zh_CN.UTF-8')  
    # 隐身模式（无痕模式）
    option.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)