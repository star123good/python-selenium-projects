from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import string
from datetime import datetime, timezone, timedelta
import json
import os
import requests



class SuperphoneScrapeContacts:
    '''
    Superphone Scrape Contacts
    '''
    superphone_url = "https://app.superphone.io/"
    login_url = superphone_url + "login/"
    contact_url = superphone_url + "contacts"

    def __init__(self, email="lancecoleman91@gmail.com", password="wecandoit!"):
        self.driver = None
        self.login_email = email
        self.login_password = password

    def openBrowser(self):
        # chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")

        # chrome self.driver
        self.driver = webdriver.Chrome("./chromedriver", options=chrome_options)
        self.driver.get(self.login_url)
        time.sleep(10)

    def login(self):
        if self.driver is None: return
        # login
        self.driver.find_element_by_id("email").send_keys(self.login_email)
        time.sleep(1)
        self.driver.find_element_by_id("password").send_keys(self.login_password)
        time.sleep(2)
        
        # submit
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(25)

    def download(self):
        if self.driver is None: return
        # open contact page
        try:
            self.driver.get(self.contact_url)
            time.sleep(20)

            # click download contact button
            download_button = self.driver.find_element_by_css_selector(".action-menu span#export-icon")
            self.driver.execute_script("arguments[0].click();", download_button)
            time.sleep(5)

            # download
            print("open download dialog")
            export_buttons = self.driver.find_elements_by_css_selector(".SpModalContent button.sp-button")
            for btn in export_buttons:
                print("button text is", btn.text)
                if btn.text.upper() == "EXPORT":
                    btn.click()
                    print("download started")
                    time.sleep(30)
                    break
        except Exception as e:
            print(e)
 
    def closeBrowser(self):
        if self.driver is None: return
        self.driver.quit()

    def run(self):
        try:
            self.openBrowser()
            self.login()
            self.download()
        except Exception as e:
            print(e)
        finally:
            self.closeBrowser()



if __name__ == "__main__":
    handler = SuperphoneScrapeContacts()
    handler.run()
