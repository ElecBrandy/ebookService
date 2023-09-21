from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# CSV로 저장
def save_to_csv(data_dict, filename):
    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=True, index_label='row_data')

# 다음 페이지로 이동
def get_next_page(driver):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(2)
	try:
		button_goNext = driver.find_element(By.CSS_SELECTOR, "#coverPagenation > div:nth-child(1) > button:nth-child(8)")
		actions = ActionChains(driver).move_to_element(button_goNext)
		actions.perform()
		button_goNext.click()
	except:
		print("button go_Next can not find")

# 마지막 페이지 확인
def get_last_page(driver, url):
	driver.get(url)
	time.sleep(2)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	try:
		button_goLast = driver.find_element(By.CSS_SELECTOR, "#coverPagenation > div:nth-child(1) > button:nth-child(9)")
		actions = ActionChains(driver).move_to_element(button_goLast)
		actions.perform()
		button_goLast.click()
	except:
		print("button go_Last can not find")
	time.sleep(2)
	soup = bs(driver.page_source, 'html.parser')
	last_number = int(soup.select_one("#coverPagenation > div:nth-child(1) > a:nth-child(3)").get_text())
	return last_number

# 테마별 링크 수집
def get_url_theme(driver, category_number, url_list):
	# 마지막 페이지 확인
	url = f'https://elib.seoul.go.kr/contents/list?t=EB&m={category_number}'
	print(f"seoul 테마별 링크 수집 중 : {url}")
	last_page = get_last_page(driver, url)

	# 테마별 링크 수집
	driver.get(url)
	time.sleep(2)
	driver.save_screenshot("c.png")
	for i in range(0, last_page):
		time.sleep(2)
		print(f"테마별 링크 수집 page : {i}")
		soup = bs(driver.page_source, 'html.parser')
		temp = soup.find("div", class_="main-contents-book4")
		a_tags = temp.find_all("a", href=True)
		for a_tag in a_tags:
			print(a_tag["href"])
			url_list.append(a_tag["href"])
		get_next_page(driver)
		time.sleep(2)

# 전체 링크 수집
def get_seoul_url_all(driver):
	url_list = []
	# 모든 테마 (001:가정과생활 ~ 019:대학교재)
	for i in range(1, 20):
		get_url_theme(driver, str(i).zfill(3), url_list)
		time.sleep(1)
	return url_list

# 전체 정보 수집 (링크 기반)
# | index | 제목 | 지은이 | 출판사 | 출판일 | 출판일자 | ISBN | 파일 유형 | 전자도서관 | 링크 |
def get_seoul_data(driver, dict, url):
	driver.get(url)
	time.sleep(1)
	# 제목
	title = driver.find_element(By.CSS_SELECTOR,'.book_detail_subject').text
	dict['제목'].append(title)

	# 지은이
	writer = driver.find_element(By.CSS_SELECTOR,'li.after:nth-child(1) > p:nth-child(2)').text
	dict['지은이'].append(writer)

	# 출판사
	publisher = driver.find_element(By.CSS_SELECTOR,'li.after:nth-child(2) > p:nth-child(2)').text
	dict['출판사'].append(publisher)

	# 출판일
	date = driver.find_element(By.CSS_SELECTOR,'li.after:nth-child(3) > p:nth-child(2)').text
	dict['출판일'].append(date)

	# ISBN
	isbn = driver.find_element(By.CSS_SELECTOR,'li.after:nth-child(4) > p:nth-child(2)').text
	dict['ISBN'].append(isbn)

	# 파일유형
	type = driver.find_element(By.CSS_SELECTOR,'li.after:nth-child(8) > p:nth-child(2)').text
	dict['파일유형'].append(type)

	# 전자도서관
	library = "서울전자도서관"
	dict['전자도서관'].append(library)

	# 링크
	link = url
	dict['링크'].append(link)

def get_seoul_data_all(driver, dict):
	url_list = get_seoul_url_all(driver)
	url_dict = {'urls': url_list}
	save_to_csv(url_dict, "seoul_url_list.scv")

	for i in url_list:
		url = f'https://elib.seoul.go.kr/contents/{i}'
		print(f"현재 스크래핑 중인 url : {url}")
		get_seoul_data(driver, dict, url)
		save_to_csv(dict, "seoul.scv")


# driver = main.selenium_driver()
# url_list = []
# get_url_theme(driver, "004", url_list)
# print(url_list)
