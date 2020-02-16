import ssl
from urllib.error import HTTPError
from selenium import webdriver
import re
# 내장함수
import os
from urllib.request import urlopen
import urllib.request
# 명령행 파싱 모듈 argparse 모듈 사용
import argparse
# request => 요청하는거를 웹에 요청한 결과값을 얻어올수 있는 모듈
import requests as req
# 웹에 요청한 결과를 보내주는 모듈
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


def google_img_crawling(keyword):
    # chrome option 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    # driver 생성
    driver = webdriver.Chrome('C:/Users/ehdus/Downloads/chromedriver.exe', options=options)
    # google 이미지 접속
    driver.get('https://www.google.co.kr/imghp?hl=ko&tab=ri&ogbl')

    # google 검색창에 키워드 입력
    driver.find_element_by_name('q').send_keys(keyword)
    driver.find_element_by_css_selector('button').click()

    try:
        img_data = []
        for i in range(1, 20):
            elem = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%d]/a[1]/div[1]/img' % (i,))
            driver.execute_script('arguments[0].click();', elem)
            # //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
            image = driver.find_elements_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img')
            # //*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img
            for img in image:
                img_src = img.get_attribute('src')
                img_data.append(img_src)
                # print(img_src)

        header = {'User-Agent': 'Mozilla/5.0', 'referer': 'https://www.google.com'}
        context = ssl._create_unverified_context()
        i = 1
        for link in (img_data):
            if 'http' in str(link) and 'encrypted' not in str(link):  # 내부에 있는 항목들을 리스트로 가져옴
                try:
                    req = urllib.request.Request(link, headers=header)
                    t = urlopen(req, context=context).read()
                    t = urlopen(link).read()
                    # print('t', t)

                    filename = people + str(i) + '.jpg'
                    save_dir = os.path.join('..', 'dataset')
                    if not os.path.exists(save_dir):
                        os.mkdir(save_dir)
                    else:
                        save_img = os.path.join(save_dir, filename)
                        with open(save_img, "wb") as f:
                            f.write(t)
                        print("Img Save Success")
                        i += 1
                except HTTPError as e:
                    print(e)
                else:
                    continue
    except NoSuchElementException:
        pass


if __name__ == '__main__':
    google_img_crawling('cat')

