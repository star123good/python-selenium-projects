from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import pandas as pd
import time
import sys


# running command sample
# python auto_upload_images_redbubble.py xlsx_file_path email password


# config
SITE_URL = 'https://www.redbubble.com/'
SITE_LOGIN_URL = SITE_URL + 'auth/login/'
SITE_UPLOAD_URL = SITE_URL + 'portfolio/images/new?ref=account-nav-dropdown/'
USER_EMAIL = ''
USER_PASSWORD = ''
CHROMEDRIVER_PATH = 'chromedriver.exe'
DEFAULT_XLSX_PATH = '10-29-19.xlsx'


# run chrome
def run_chrome(df):
    try:
        # chrome driver
        driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        driver.maximize_window()

        # login
        driver.get(SITE_LOGIN_URL)
        time.sleep(10)
        driver.find_element_by_xpath("//input[@id='ReduxFormInput1']").send_keys(USER_EMAIL)
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='ReduxFormInput2']").send_keys(USER_PASSWORD)
        time.sleep(2)
        driver.find_element_by_xpath("//button[@class='app-ui-components-Button-Button_button_1_MpP app-ui-components-Button-Button_primary_pyjm6 app-ui-components-Button-Button_padded_1fH5b']").click()
        time.sleep(100)

        # upload image
        # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "app")))
        # time.sleep(2)
        for index, row in df.iterrows():
            driver.get(SITE_UPLOAD_URL)
            time.sleep(10)
            driver.find_element_by_xpath("//input[@id='select-image-single']").send_keys(row['Image Path'])
            time.sleep(10)
            driver.find_element_by_xpath("//input[@id='work_title_en']").send_keys(row['Title'])
            time.sleep(1)
            driver.find_element_by_xpath("//textarea[@id='work_tag_field_en']").send_keys(row['Tags'])
            time.sleep(1)
            driver.find_element_by_xpath("//textarea[@id='work_description_en']").send_keys(row['Description'])
            time.sleep(3)
            driver.find_element_by_xpath("//input[@id='work_safe_for_work_false']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//input[@id='rightsDeclaration']").click()
            time.sleep(2)
            driver.find_element_by_xpath("//input[@id='submit-work']").click()
            time.sleep(30)

        # edit title, tags, descriptions

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