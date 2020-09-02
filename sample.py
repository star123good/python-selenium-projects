from selenium import webdriver
import time


# driver = webdriver.Chrome("D:/Development Tools/Python & Django/Selenium/chromedriver.exe")
driver = webdriver.Chrome("./chromedriver")
driver.get("https://stackoverflow.com/questions/33150351/how-do-i-install-chromedriver-on-windows-10-and-run-selenium-tests-with-chrome")


time.sleep(100)
driver.quit()