import os
import base64
from selenium import webdriver
from django.http import HttpResponse

def get_weather_widget(location):
    if '제주' in location:
        location = '제주시'
    
    location += ' '
    weather = '날씨'
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={}+{}'.format(location, weather)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe')
    
    driver = webdriver.Chrome(path, chrome_options=chrome_options)
    driver.get(url)

    element = driver.find_element_by_class_name('main_info')
    element_png = element.screenshot_as_base64

    return element_png