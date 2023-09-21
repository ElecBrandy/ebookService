from selenium import webdriver
import os
import scrapSeoul
import scrapYes

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

# | index | 제목 | 지은이 | 출판사 | 출판일 | ISBN | 파일 유형 | 전자도서관 |

# 메인 함수
def main():
    driver = selenium_driver()
    # df_snu = pd.read_csv('./csv/snu.csv', encoding='utf-8')
    seoul_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], 'ISBN' : [], '파일유형' : [], '전자도서관' : [], '링크' : []}
    yes_dict = {'제목': [], '지은이': [], '출판사': [], '출판일': [], 'ISBN' : [], '파일유형' : [], '전자도서관' : [], '링크' : []}

    #scrapSeoul.get_seoul_data_all(driver, seoul_dict)
    scrapYes.get_yes_data_all(driver, yes_dict)
    driver.quit()

if __name__ == "__main__":
    main()
