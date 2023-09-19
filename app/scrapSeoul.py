from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time

# 마지막 페이지 확인
def scroll_down_last(driver):
	wait = WebDriverWait(driver, 20)
	try:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		button_goLast = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#coverPagenation > div:nth-child(1) > button:nth-child(9)")))
		actions = ActionChains(driver).move_to_element(button_goLast)
		actions.perform()
		button_goLast.click()
	except:
		print("button go_Last can not find")

# 다음 페이지로 이동
def scroll_down_next(driver):
	wait = WebDriverWait(driver, 10)
	try:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		button_goNext = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#coverPagenation > div:nth-child(1) > button:nth-child(8)")))
		actions = ActionChains(driver).move_to_element(button_goNext)
		actions.perform()
		button_goNext.click()
	except:
		print("button go_Next can not find")

def get_last_page(driver, url):
	driver.get(url)
	time.sleep(1)
	scroll_down_last(driver)
	time.sleep(5)
	driver.save_screenshot('./a.jpg')
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	soup = bs(driver.page_source, 'html.parser')
	last_number = int(soup.select_one("#coverPagenation > div:nth-child(1) > a:nth-child(3)").get_text())
	return last_number

def get_url_seoul(driver, category_number):
	url_list = []
	last_page = 0

	# Bs4 // {page_number} = 장르를 의미
	url = f'https://elib.seoul.go.kr/contents/list?t=EB&m={category_number}'
	print(url)
	last_page = get_last_page(driver, url)
	print(last_page)

	driver.get(url)

	i = 0
	while (i < last_page):
		print(i)
		soup = bs(driver.page_source, 'html.parser')
		temp = soup.find("div", class_="main-contents-book4")
		a_tags = temp.find_all("a", href=True)
		for a_tag in a_tags:
			url_list.append(a_tag["href"])
		scroll_down_next(driver)
		time.sleep(2)
		i = i + 1
	print(len(url_list))
	return url_list

# 메인
def seoul(driver):

	get_url_seoul(driver, str(1).zfill(3))
	driver.quit()

# content_total_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], 'ISBN': [], '파일 유형': [], '전자도서관': [], '링크': []}

seoul(content_total_dict)

print(content_total_dict['링크'])


