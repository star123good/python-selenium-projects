from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import pandas as pd
import time
import sys


# running command sample
# python auto_upload_images_spreadshirt.py xlsx_file_path email password


# config
SITE_URL = 'https://www.spreadshirt.com/'
SITE_PARTNER_URL = 'https://partner.spreadshirt.com/'
SITE_LOGIN_URL = SITE_URL + 'login'
SITE_UPLOAD_URL = SITE_PARTNER_URL + 'designs'
USER_EMAIL = ''
USER_PASSWORD = ''
CHROMEDRIVER_PATH = 'chromedriver.exe'
DEFAULT_XLSX_PATH = '11-13-19.xlsx'


# run chrome
def run_chrome(df):
    try:
        # chrome driver
        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.maximize_window()

        # login
        driver.get(SITE_LOGIN_URL)
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "loginForm")))
        time.sleep(6)
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[@id='central-login-iframe']"))
        driver.find_element_by_xpath("//input[@id='username']").send_keys(USER_EMAIL)
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(USER_PASSWORD)
        time.sleep(2)
        driver.find_element_by_xpath("//button[@id='login-submit']").click()
        time.sleep(5)
        # driver.switch_to.default_content()
        
        # partner url
        driver.get(SITE_UPLOAD_URL)
        time.sleep(6)

        # upload image
        for index, row in df.iterrows():
            # driver.get(SITE_UPLOAD_URL)
            time.sleep(5)
            if index == 0: 
                driver.find_element_by_xpath("//a[@id='upload-btn']").click()
            else:
                driver.find_element_by_xpath("//button[@class='btn btn-primary icon-btn']").click()
            time.sleep(3)
            driver.find_element_by_xpath("//input[@ngf-drag-over-class='dragover']").send_keys(row['Image Path'])
            time.sleep(10)
            driver.find_element_by_xpath("//div[@class='image-wrapper']").click()
            time.sleep(5)
            driver.find_element_by_xpath("//button[@id='account-settings-save-button']").click()
            time.sleep(3)
            # edit title, tags, descriptions
            driver.find_element_by_xpath("//input[@id='input-design-name']").clear()
            driver.find_element_by_xpath("//input[@id='input-design-name']").send_keys(row['Title'])
            time.sleep(1)
            driver.find_element_by_xpath("//textarea[@id='input-design-description']").send_keys(row['Description'])
            time.sleep(1)
            driver.find_element_by_xpath("//input[@class='dropdown-input']").send_keys(row['Tags'])
            time.sleep(3)
            driver.find_element_by_xpath("//button[@id='account-settings-save-button']").click()
            time.sleep(10)

        # quit
        time.sleep(100)
        driver.quit()
    except Exception as e:
        print(e)
        print('Please try again.')

# main
def main():
    # read xlsx file
    try:
        # print(DEFAULT_XLSX_PATH)
        df = pd.read_excel(DEFAULT_XLSX_PATH)
        df = df.dropna()
        if df.empty == True:
            print("There is no data in the selected xlsx file.")
        else:
            # run chrome
            run_chrome(df)
        
        
    except Exception as e:
        print(e)
        print('You must input correct path of xlsx file.')

# call main
if __name__ == "__main__":
    # input xlsx file path
    if len(sys.argv) > 1:
        DEFAULT_XLSX_PATH = sys.argv[1]
    # input user email
    if len(sys.argv) > 2:
        USER_EMAIL = sys.argv[2]
    # input user password
    if len(sys.argv) > 3:
        USER_PASSWORD = sys.argv[3]
    main()