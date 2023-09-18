from selenium import webdriver
from bs4 import BeautifulSoup as bs
from collections import Counter
import pandas as pd
import time
import os
import ast
import main

# Selenium 설정
def selenium_driver():
    options = webdriver.FirefoxOptions()
    options.headless = True
    firefox_binary_path = "/usr/bin/firefox-esr"
    options.binary_location = firefox_binary_path

    display_port = os.environ.get("DISPLAY_PORT", "99")
    display = f":{display_port}"
    os.environ["DISPLAY"] = display

    xvfb_cmd = f"Xvfb {display} -screen 0 1920x1080x24 -nolisten tcp &"
    os.system(xvfb_cmd)

    return webdriver.Firefox(options=options)

# CSV로 저장
def save_to_csv(data_dict, filename):
    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=True, index_label='row_data')

# | index | 제목 | 지은이 | 출판사 | 출판일 | 파일 유형 | 전자도서관 |

# 메인 함수
def main():
    driver = selenium_driver()

    df_snu = pd.read_csv('./csv/snu.csv', encoding='utf-8')
    content_total_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], '파일 유형' : [], '전자도서관' : []}

    for i in df_snu['상세내용']:
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
