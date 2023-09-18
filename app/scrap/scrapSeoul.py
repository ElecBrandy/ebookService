from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from collections import Counter
import pandas as pd
import time
import os
import ast
import main

def get_url(driver, page_number):
    urls = []
    page_count = 1
    last_number = 0

    # Bs4
    url = f'https://elib.seoul.go.kr/contents/list?t=EB&m={page_number}'
    driver.get(url)
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')

    # 마지막 페이지 확인
    driver.find_element(By.XPATH, '//*[@id="goLast"]')
    last_number = soup.select_one("#coverPagenation > div:nth-child(1) > a:nth-child(3)")
    driver.find_element(By.XPATH, '//*[@id="goFirst"]')

    # 링크 추출
    urls_tags = soup.select('.book_list > li:nth-child(1) > div:nth-child(1) > a:nth-child(2)')
    for urls in urls_tags:
        urls.append(urls['href'])
        if page_count >= last_number:
            break


    return urls


# 메인 함수
# | index | 제목 | 지은이 | 출판사 | 출판일 | 파일 유형 | 전자도서관 |
def main_seoul():
    driver = main.selenium_driver()

    df_seoul = pd.read_csv('./csv/seoul.csv', encoding='utf-8')
    content_total_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], '파일 유형' : [], '전자도서관' : []}

    for i in df_seoul['상세내용']:
        temp = ast.literal_eval(i)
        keyword_list = get_top_n_frequencies(temp, top_keywords)
        combine = ', '.join(keyword_list)

        url_list = get_url_list(driver, combine, news_per_keyword)

        for url in url_list:
            get_news_info(driver, url, content_total_dict)

        save_to_csv(content_total_dict, 'intermediate.csv')

    driver.quit()

if __name__ == "__main__":
    main()
