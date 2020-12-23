from selenium import webdriver
import time


option = webdriver.ChromeOptions()
option.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome("./chromedriver",options=option)
driver.get("https://passport.zhaopin.com/org/login")

# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

time.sleep(100)
driver.quit()