from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re

# http://yes24new.yes24library.com/

# CSV로 저장
def save_to_csv(data_dict, filename):
    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=True, index_label='row_data')

def yes_author(text):
	if ' 저' in text:
		pattern = r"<(.*?)> 저"
	elif '편' in text:
		pattern = r"<(.*?)> 편"
	else:
		return text
	authors = re.findall(pattern, text)
	authors_list = []
	for author in authors:
		cleaned_author = author.replace("<", "").replace(">", "").strip()
		authors_list.append(cleaned_author)
		result = ", ".join(authors_list)
	if result:
		return result
	else:
		return text

# 테마별 링크 수집
def get_url_theme(driver, category_number, url_list):
	# 마지막 페이지 확인
	url = f'http://yes24new.yes24library.com/ebook/?code=category&mode=&sort=&cate_id={category_number}&page_num=1&view=600#list_tab'
	print(f"yes24 테마별 링크 수집 중 : {url}")

	# 테마별 링크 수집
	driver.get(url)
	time.sleep(2)
	driver.save_screenshot("a.png")

	time.sleep(2)
	soup = bs(driver.page_source, 'html.parser')
	temp = soup.find('div', id='booklist')
	a_tags = temp.select('.book_tit a[href]')
	for a_tag in a_tags:
		print(a_tag["href"])
		url_list.append(a_tag["href"])

# 전체 링크 수집
def get_yes_url_all(driver):
	url_list = []
	category_list = [1, 2, 3, 4, 5, 9, 10, 11, 12 ,13, 14, 15, 23, 28]
	# 모든 테마 (001:인문사회 ~ 028:만화)
	for i in category_list:
		get_url_theme(driver, str(i).zfill(3), url_list)
		time.sleep(1)
	return url_list

# 전체 정보 수집 (링크 기반)
# | index | 제목 | 지은이 | 출판사 | 출판일 | 출판일자 | ISBN | 파일 유형 | 전자도서관 | 링크 |
def get_yes_data(driver, dict, url):
	driver.get(url)
	time.sleep(1)
	driver.save_screenshot("b.png")
	# 제목
	title = driver.find_element(By.CSS_SELECTOR,'div.tit').text
	dict['제목'].append(title)

	# 지은이
	try:
		author = driver.find_element(By.CSS_SELECTOR, 'div.cont:nth-child(3) > ul:nth-child(2) > li:nth-child(1)').text[3:]
		author_clean = yes_author(author)
		dict['지은이'].append(author_clean)
	except NoSuchElementException:
		try:
			author = driver.find_element(By.CSS_SELECTOR, '#bookview > div:nth-child(2) > ul:nth-child(2) > li:nth-child(1)').text[3:]
			author_clean = yes_author(author)
			dict['지은이'].append(author_clean)
		except NoSuchElementException:
			dict['지은이'].append("0")

	# 출판사
	try:
		publisher = driver.find_element(By.CSS_SELECTOR, 'div.cont:nth-child(3) > ul:nth-child(2) > li:nth-child(2)').text[4:]
		dict['출판사'].append(publisher)
	except NoSuchElementException:
		try:
			publisher = driver.find_element(By.CSS_SELECTOR, '#bookview > div:nth-child(2) > ul:nth-child(2) > li:nth-child(2)').text[4:]
			dict['출판사'].append(publisher)
		except NoSuchElementException:
			dict['출판사'].append("0")

	# 출판일
	try:
		date = driver.find_element(By.CSS_SELECTOR,'div.cont:nth-child(3) > ul:nth-child(2) > li:nth-child(3)').text[4:]
		dict['출판일'].append(date)
	except NoSuchElementException:
		try:
			date = driver.find_element(By.CSS_SELECTOR,'#bookview > div:nth-child(2) > ul:nth-child(2) > li:nth-child(3)').text[4:]
			dict['출판일'].append(date)
		except NoSuchElementException:
			dict['출판일'].append("0")

	# ISBN
	isbn = "0"
	dict['ISBN'].append(isbn)

	# 파일유형
	try:
		type = driver.find_element(By.CSS_SELECTOR,'.dotline > li:nth-child(2)').text[5:]
		dict['파일유형'].append(type)
	except NoSuchElementException:
		dict['파일유형'].append("0")

	# 전자도서관
	library = "yes24전자도서관"
	dict['전자도서관'].append(library)

	# 링크
	link = url
	dict['링크'].append(link)

def get_yes_data_all(driver, dict):
	# url_list = get_yes_url_all(driver)
	# url_dict = {'urls': url_list}
	# save_to_csv(url_dict, "yes_url_list.scv")

	# /{i/} = /ebook/detail?goods_id=101387224
	temp = pd.read_csv('/workspaces/ebookService/app/yes_url_list.scv', encoding='utf-8')
	for i in temp['urls']:
		url = f'http://yes24new.yes24library.com{i}'
		print(f"현재 스크래핑 중인 url : {url}")
		get_yes_data(driver, dict, url)
		save_to_csv(dict, "yes.scv")


# import main
# driver = main.selenium_driver()
# url_list = []
# get_url_theme(driver, "004", url_list)
# print(url_list)


# def get_url_theme(driver, category_number, url_list):
