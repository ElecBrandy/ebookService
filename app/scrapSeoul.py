from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import ast
import main

def scroll_element_to_bottom(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

def get_url_seoul(driver, page_number):
    urls = []
    page_count = 1
    last_number = 0

    # Bs4 // {page_number} = 장르를 의미
    url = f'https://elib.seoul.go.kr/contents/list?t=EB&m={page_number}'
    driver.get(url)
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    print(url)
    
    # 마지막 페이지 확인
    driver.find_element(By.CSS_SELECTOR, '.main-contents').click()
    try:
        # "goLast" 버튼을 화면에 스크롤하여 보이도록 하고 클릭
        element = driver.find_element(By.ID, 'goLast')
        scroll_element_to_bottom(driver, element)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.ID, 'goLast').click()
        time.sleep(1)
        print("성공")
    except:
        # 요소를 찾지 못했을 때의 메시지
        print("요소를 찾지 못했습니다.")

    time.sleep(1)
    last_number = soup.select_one("#coverPagenation > div:nth-child(1) > a:nth-child(3)")
    driver.find_element(By.CSS_SELECTOR, '#coverPagenation > div:nth-child(1) > button:nth-child(1)').click()
    time.sleep(1)
    print("asdf")
    print(last_number)
    print("\n")

    # 페이지 순회하며 링크 수집
    while (page_count <= last_number):
        urls_tags = soup.select('.book_list > li:nth-child(1) > div:nth-child(1) > a:nth-child(2)')
        for url_tag in urls_tags:
            urls.append(url_tag['href'])
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.find_element(By.XPATH, '//*[@id="goNext"]').click()
        time.sleep(2)
        page_count += 1
    
    return urls

# 메인 함수
def seoul(content_total_dict):
    driver = main.selenium_driver()

    for i in range(1, 20): 
        # '링크'에 해당하는 부분에 함수 'get_url_seoul'의 결과값을 추가
        content_total_dict['링크'].extend(get_url_seoul(driver, str(i).zfill(3)))

    main.save_to_csv(content_total_dict, 'seoul.csv')

    driver.quit()

content_total_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], 'ISBN': [], '파일 유형': [], '전자도서관': [], '링크': []}
seoul(content_total_dict)
