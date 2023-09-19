from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

page_number = 1
# Bs4 // {page_number} = 장르를 의미
url = f'https://elib.seoul.go.kr/contents/list?t=EB&m={page_number}'
driver.get(url)
time.sleep(1)
soup = bs(driver.page_source, 'html.parser')
print(url)

try:
    # "goLast" 버튼을 화면에 스크롤하여 보이도록 하고 클릭
    element = driver.find_element(By.ID, 'goLast')
    scroll_element_to_bottom(driver, element)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    for i in (0, 50):
        driver.key_down(Keys.PAGE_DOWN).perform()
        driver.key_up(Keys.PAGE_DOWN).perform()

    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'pages').click()
    time.sleep(1)
    print("성공")
except:
    # 요소를 찾지 못했을 때의 메시지
    print("요소를 찾지 못했습니다.")
