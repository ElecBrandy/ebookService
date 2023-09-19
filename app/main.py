from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from collections import Counter
import pandas as pd
import time
import os
import ast

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

# | index | 제목 | 지은이 | 출판사 | 출판일 | ISBN | 파일 유형 | 전자도서관 |

# 메인 함수
def main():
    driver = selenium_driver()
    # df_snu = pd.read_csv('./csv/snu.csv', encoding='utf-8')
    total_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], 'ISBN' : [], '파일 유형' : [], '전자도서관' : [], '링크' : []}


    driver.quit()



if __name__ == "__main__":
    main()
