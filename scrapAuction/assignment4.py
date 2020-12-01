#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime as dt
# import pandas as pd
from time import sleep
import sqlite3
from threading import *


# In[2]:


import os
# os.chdir('Automation')


# In[3]:


#sqlite3 databse creating:
conn = sqlite3.connect('copart.db')
c = conn.cursor()

# create table if not there
try:
    c.execute('''CREATE TABLE carsdata(model TEXT PRIMARY KEY, location TEXT,doctype TEXT,odometer TEXT,rstretailvalue TEXT, sublotlocation TEXT, primarydamage TEXT, secondarydamage TEXT, highlights TEXT, bodystyle TEXT, color TEXT, enginetype TEXT, cylinders TEXT, drive TEXT, fuel TEXT, keys TEXT, specialnote TEXT, price TEXT )''')
except:
    pass


# In[9]:


# driver setup..................................

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

options = webdriver.ChromeOptions()

# options.headless = True
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
options.add_experimental_option("prefs", prefs)
#driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver.exe')


# In[10]:


# initiating the webdriver
driver = webdriver.Chrome(options=options, executable_path="chromedriver")

# Targeting the website
driver.maximize_window()
#url = "https://www.copart.com/todaysAuction/" # https://www.copart.com/todaysAuction/
url  = "https://www.copart.com/todaysAuction"
driver.get(url)


# In[8]:


results = driver.find_elements_by_css_selector("div[class='btn btn-green joinsearch small']")
for j in results:
    print(j.get_attribute('href'))
    try:
        scrapeone(j.get_attribute("href")) # webdriver 2 task
    except:
        pass
    links.append(j.get_attribute("href"))


# In[55]:


model = driver.find_element_by_xpath('/html/body/div[2]/root/app-root/div/widget-area/div[2]/div[3]/div/gridster/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[1]/lot-header/section/div[1]/div[1]')
model.text


# In[49]:


def auctionscraper(i):
    #clicking the join now button
    driver.find_elements_by_xpath('//*[@id="auctionLiveNow-datatable"]/tbody/tr[' + i + ']/td[9]/ul/li[1]/a')[0].click()

    #wait until the table loads
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="lotDesc-COPART004C"]/div[1]/div[1]')))

    carsleft = 999999999

    while True:
        try:
            Model = driver.find_element_by_xpath('//*[@id="lotDesc-COPART004C"]/div[1]/div[1]').text
        except:
            pass
        try:
            Location = driver.find_element_by_id('copart_COPART189A_yardName_mini').text
        except:
            pass
        try:
            DocType = driver.find_element_by_id('copart_COPART189A_docType_mini').text
        except:
            pass
        try:
            Odometer = driver.find_element_by_id('copart_COPART189A_odometer_mini').text
        except:
            pass
        try:
            EstRetailValue = driver.find_element_by_id('copart_COPART189A_retailValue-currencyFormat_mini').text
        except:
            pass
        try:
            SublotLocation = driver.find_element_by_id('copart_COPART189A_subLot_mini').text
        except:
            pass
        try:
            PrimaryDamage = driver.find_element_by_id('copart_COPART189A_primaryDamage_mini').text
        except:
            pass
        try:
            SecondaryDamage = driver.find_element_by_id('copart_COPART189A_secondaryDamage_mini').text
        except:
            pass
        try:
            Highlights = driver.find_element_by_id('copart_COPART189A_lotDetailIconCodes_mini').text
        except:
            pass
        try:
            BodyStyle = driver.find_element_by_id('copart_COPART189A_bodyStyle_mini').text
        except:
            pass
        try:
            Color = driver.find_element_by_id('copart_COPART189A_color_mini').text
        except:
            pass
        try:
            EngineType = driver.find_element_by_id('copart_COPART189A_engine_mini').text
        except:
            pass
        try:
            Cylinders = driver.find_element_by_id('copart_COPART189A_cylinders_mini').text
        except:
            pass
        try:
            Drive = driver.find_element_by_id('copart_COPART189A_drive_mini').text
        except:
            pass
        try:
            Fuel = driver.find_element_by_id('copart_COPART189A_fuel_mini').text
        except:
            pass
        try:
            Keys = driver.find_element_by_id('copart_COPART189A_keys_mini').text
        except:
            pass
        try:
            SpecialNote = driver.find_element_by_id('copart_COPART189A_specialNote_mini').text
        except:
            pass
        try:
            LivePrice = driver.find_element_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]').text
        except:
            pass
        try:
            carsleft = driver.find_element_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]').text
        except:
            pass

        # inserting data(if exits will replace price)
        if Model_lastiteration != Model:
            c.execute('''INSERT INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))
        else:
            c.execute('''REPLACE INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))

        #saving the last iteration:
        Model_lastiteration = Model
        sleep(.5)

print(model)


# In[40]:


Model_lastiteration = "test3"
Model = "test"
Location = "test"
DocType = "test"
Odometer ="test"
EstRetailValue ="test"
SublotLocation = "test"
PrimaryDamage = "test"
SecondaryDamage ="test"
Highlights = "test"
BodyStyle = "test"
Color ="test"
EngineType = "test"
Cylinders = "testc"
Drive = "test"
Fuel ="test"
Keys ="test"
SpacialNote ="test"
LivePrice ="test"


# In[44]:


# clicking the join now button
#driver.find_elements_by_xpath('//*[@id="auctionLiveNow-datatable"]/tbody/tr/td[9]/ul/li[1]/a')[0].click()

#wait until the table loads
#wait = WebDriverWait(driver, 100)
#wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="lotDesc-COPART004C"]/div[1]/div[1]')))

#carsleft = 999999999
Model = driver.find_element_by_class_name('titlelbl  ellipsis').text

while True:
    try:
        Model = driver.find_element_by_xpath('/html/body/div[2]/root/app-root/div/widget-area/div[2]/div[3]/div/gridster/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[1]/lot-header/section/div[1]/div[1]').text
    except:
        pass
    try:
        Location = driver.find_element_by_id('copart_COPART189A_yardName_mini').text
    except:
        pass
    try:
        DocType = driver.find_element_by_id('copart_COPART189A_docType_mini').text
    except:
        pass
    try:
        Odometer = driver.find_element_by_id('copart_COPART189A_odometer_mini').text
    except:
        pass
    try:
        EstRetailValue = driver.find_element_by_id('copart_COPART189A_retailValue-currencyFormat_mini').text
    except:
        pass
    try:
        SublotLocation = driver.find_element_by_id('copart_COPART189A_subLot_mini').text
    except:
        pass
    try:
        PrimaryDamage = driver.find_element_by_id('copart_COPART189A_primaryDamage_mini').text
    except:
        pass
    try:
        SecondaryDamage = driver.find_element_by_id('copart_COPART189A_secondaryDamage_mini').text
    except:
        pass
    try:
        Highlights = driver.find_element_by_id('copart_COPART189A_lotDetailIconCodes_mini').text
    except:
        pass
    try:
        BodyStyle = driver.find_element_by_id('copart_COPART189A_bodyStyle_mini').text
    except:
        pass
    try:
        Color = driver.find_element_by_id('copart_COPART189A_color_mini').text
    except:
        pass
    try:
        EngineType = driver.find_element_by_id('copart_COPART189A_engine_mini').text
    except:
        pass
    try:
        Cylinders = driver.find_element_by_id('copart_COPART189A_cylinders_mini').text
    except:
        pass
    try:
        Drive = driver.find_element_by_id('copart_COPART189A_drive_mini').text
    except:
        pass
    try:
        Fuel = driver.find_element_by_id('copart_COPART189A_fuel_mini').text
    except:
        pass
    try:
        Keys = driver.find_element_by_id('copart_COPART189A_keys_mini').text
    except:
        pass
    try:
        SpecialNote = driver.find_element_by_id('copart_COPART189A_specialNote_mini').text
    except:
        pass
    try:
        LivePrice = driver.find_element_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]').text
    except:
        pass
    try:
        carsleft = driver.find_element_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]').text
    except:
        pass

    # inserting data(if exits will replace price)
#     if Model_lastiteration != Model:
#         c.execute('''INSERT INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))
#     else:
#         c.execute('''REPLACE INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))

#     #saving the last iteration:
#     Model_lastiteration = Model
    print(f"Model Name: {Model}")

    sleep(1)


# In[58]:


def startthread(i):
    auc_scraper = auctionscraper(i)
    t1 = Thread(target = auc_scraper)
    t1.start()


# In[5]:


#wait until the table loads
wait = WebDriverWait(driver, 100)
wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="auctionLiveNow-datatable"]/tbody/tr[1]/td[9]/ul/li[1]/a')))

noofliveauctions_string = driver.find_element_by_id('auctionLiveNow-datatable_info').text.split()[3]
noofliveauctions = int(noofliveauctions_string)

for i in range(noofiterations):
    startthread(i)
    i += 1


# auvtion table no of rows = auctionLiveNow-datatable_info
#join auction         = //*[@id="auctionLiveNow-datatable"]/tbody/tr[1]/td[9]/ul/li[1]/a
#join auction 2nd row = //*[@id="auctionLiveNow-datatable"]/tbody/tr[2]/td[9]/ul/li[1]/a
#join auction ith row = //*[@id="auctionLiveNow-datatable"]/tbody/tr[i]/td[9]/ul/li[1]/a


# In[ ]:


# Model = driver.find_element_by_xpath('//*[@id="lotDesc-COPART004C"]/div[1]/div[1]').text

# Location = driver.find_element_by_id('copart_COPART189A_yardName_mini').text
# DocType = driver.find_element_by_id('copart_COPART189A_docType_mini').text
# Odometer = driver.find_element_by_id('copart_COPART189A_odometer_mini').text
# EstRetailValue = driver.find_element_by_id('copart_COPART189A_retailValue-currencyFormat_mini').text
# SublotLocation = driver.find_element_by_id('copart_COPART189A_subLot_mini').text
# PrimaryDamage = driver.find_element_by_id('copart_COPART189A_primaryDamage_mini').text
# SecondaryDamage = driver.find_element_by_id('copart_COPART189A_secondaryDamage_mini').text
# Highlights = driver.find_element_by_id('copart_COPART189A_lotDetailIconCodes_mini').text
# BodyStyle = driver.find_element_by_id('copart_COPART189A_bodyStyle_mini').text
# Color = driver.find_element_by_id('copart_COPART189A_color_mini').text
# EngineType = driver.find_element_by_id('copart_COPART189A_engine_mini').text
# Cylinders = driver.find_element_by_id('copart_COPART189A_cylinders_mini').text
# Drive = driver.find_element_by_id('copart_COPART189A_drive_mini').text
# Fuel = driver.find_element_by_id('copart_COPART189A_fuel_mini').text
# Keys = driver.find_element_by_id('copart_COPART189A_keys_mini').text
# SpecialNote = driver.find_element_by_id('copart_COPART189A_specialNote_mini').text
# LivePrice = try:
#                 driver.find_element_by_xpath('//*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]').text
#             except:
#                 pass


# In[52]:


Model_lastiteration = "test3"
Model = "test"
Location = "test"
DocType = "test"
Odometer ="test"
EstRetailValue ="test"
SublotLocation = "test"
PrimaryDamage = "test"
SecondaryDamage ="test"
Highlights = "test"
BodyStyle = "test"
Color ="test"
EngineType = "test"
Cylinders = "testc"
Drive = "test"
Fuel ="test"
Keys ="test"
SpacialNote ="test"
LivePrice ="test"


# In[53]:


#sqlite3 databse creating:
conn = sqlite3.connect('copart.db')
c = conn.cursor()

# create table if not there
try:
    c.execute('''CREATE TABLE carsdata(model TEXT PRIMARY KEY, location TEXT,doctype TEXT,odometer TEXT,rstretailvalue TEXT, sublotlocation TEXT, primarydamage TEXT, secondarydamage TEXT, highlights TEXT, bodystyle TEXT, color TEXT, enginetype TEXT, cylinders TEXT, drive TEXT, fuel TEXT, keys TEXT, specialnote TEXT, price TEXT )''')
except:
    pass

# inserting data(if exits will replace price)
if Model_lastiteration != Model:
    c.execute('''INSERT INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))
else:
    c.execute('''REPLACE INTO carsdata VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(Model,Location,DocType,Odometer,EstRetailValue,SublotLocation,PrimaryDamage,SecondaryDamage,Highlights,BodyStyle,Color,EngineType,Cylinders,Drive,Fuel,Keys,SpacialNote,LivePrice))

c.execute('''SELECT * FROM carsdata''')
print(c.fetchall())


# In[11]:



# model = //*[@id="lotDesc-COPART004C"]/div[1]/div[1]

# location = copart_COPART189A_yardName_mini
# Doc Type = copart_COPART189A_docType_mini
# Odometer = copart_COPART189A_odometer_mini
# Est. Retail Value = copart_COPART189A_retailValue-currencyFormat_mini
# Sublot Location = copart_COPART189A_subLot_mini
# Primary Damage = copart_COPART189A_primaryDamage_mini
# Secondary Damage = copart_COPART189A_secondaryDamage_mini
# Highlights = copart_COPART189A_lotDetailIconCodes_mini
# VIN = 
# Body Style = copart_COPART189A_bodyStyle_mini
# Color = copart_COPART189A_color_mini
# Engine Type = copart_COPART189A_engine_mini
# Cylinders = copart_COPART189A_cylinders_mini
# Drive = copart_COPART189A_drive_mini
# Fuel = copart_COPART189A_fuel_mini
# Keys = copart_COPART189A_keys_mini
# Special Note = copart_COPART189A_specialNote_mini

# live price = //*[@id="gridsterComp"]/gridster-item/widget/div/div/div/div/div[2]/div[1]/div[3]/section/section/bidding-area/bidding-dialer-area/div[2]/div/div/div[1]/bidding-dialer-refactor/svg/text[1]


# In[ ]:




