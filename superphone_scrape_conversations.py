from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import string
from datetime import datetime, timezone, timedelta
import json
import os
import requests
import mysql.connector



today_now = datetime.now()
yesterday_date = (today_now - timedelta(days=1)).strftime("%Y-%m-%d")
today_datetime = today_now.strftime("%Y-%m-%d %H:%M:%S")
today_date = today_now.strftime("%Y-%m-%d")
getDateTime = lambda str : str.replace("Today", today_date+" ").replace("Yesterday", yesterday_date+" ")


class SuperphoneScrapeConversations:
    '''
    Superphone Scrape Conversations
    '''
    superphone_url = "https://app.superphone.io/"
    login_url = superphone_url + "login/"
    max_total_count = 150
    skip_start_position = 0
    delete_start_position = 1000
    # delete_pattern = '2wk ago'
    delete_pattern = '3mo ago'
    # post_url = "http://localhost:8001/conversation-add"
    post_url = "http://hitmylyne.com//conversation-add"

    def __init__(self, email="lancecoleman91@gmail.com", password="wecandoit!"):
        self.driver = None
        self.login_email = email
        self.login_password = password
        self.position = 0
        self.incoming = 0
        self.outgoing = 0
        self.flag_delete = False
        self.file = None
        self.flag_write = False

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

    def clickItem(self):
        if self.driver is None: return
        # click item
        item_pointers = self.driver.find_elements_by_css_selector(".sp-sidebaritem.conversations-item.pointer .sp-menu-item-inner")
        start_pos = self.position
        # skip
        if len(item_pointers) < self.skip_start_position:
            self.position = len(item_pointers)
            return
        try:
            for x in range(start_pos,len(item_pointers)):
                if item_pointers[x].is_displayed():
                    item_pointers[x].click()
                    time.sleep(10)
                    # get last msg
                    contact_span = item_pointers[x].find_elements_by_css_selector("span.contact-name")
                    contact_name = contact_span[0].text if len(contact_span) > 0 else ""
                    if contact_name[0] == "+":
                        contact_phone = contact_name
                        contact_name = ""
                    else:
                        contact_phone = ""
                    photo_img = item_pointers[x].find_elements_by_css_selector("div.thumbnail-wrapper.circular img")
                    contact_photo = photo_img[0].get_attribute("src") if len(photo_img) > 0 else ""
                    time_span = item_pointers[x].find_elements_by_css_selector("div.sp-t-timestamp")
                    time_stamp = time_span[0].text if len(time_span) > 0 else ""
                    details_span = item_pointers[x].find_elements_by_css_selector("span.details-text")
                    last_msg = details_span[0].text if len(details_span) > 0 else ""
                    # get conversation of item
                    convs = self.getConversation()
                    if len(convs) > 0 :
                        last_date = convs[len(convs)-1]['Date']
                    else :
                        last_date = time_stamp
                    incoming_count = self.incoming
                    outgoing_count = self.outgoing
                    result = {
                        'Name' : contact_name,
                        'Phone' : contact_phone,
                        'Photo' : contact_photo,
                        'Incoming' : incoming_count,
                        'outgoing' : outgoing_count,
                        'Message' : last_msg,
                        'Date' : last_date,
                        'messages' : convs,
                        'isDeleted' : 0,
                    }
                    # check to delete
                    self.checkDelete(pattern=time_stamp, target=self.delete_pattern)
                    # delete conversation of item
                    is_deleted = self.deleteConversation()
                    # increase position
                    if is_deleted:
                        # post data to save backend
                        result['isDeleted'] = 1
                        self.post_request(result)
                    else:
                        self.position = self.position + 1
                    # write
                    self.writeLogFile(result)
                    print(result)
        except Exception as e:
            print(e)
        
    def scrollDown(self):
        if self.driver is None: return
        # scroll down to next elements
        lazy_content = self.driver.find_element_by_class_name('lazy-content')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', lazy_content)
        time.sleep(20)

    def closeBrowser(self):
        if self.driver is None: return
        self.driver.quit()

    def getConversation(self):
        if self.driver is None: return
        # conversation list
        results = []
        self.incoming = 0
        self.outgoing = 0
        last_date = ""
        conv_list = self.driver.find_elements_by_css_selector(".conversation-message-list-container-internal .SpConversationMessageBody.sc-RWGNv.fkdzho")
        for conv_elm in conv_list:
            p_elms = conv_elm.find_elements_by_css_selector("p.m-t-20.m-b-0.small.text-center")
            div_elms = conv_elm.find_elements_by_css_selector("div.sc-gCUMDz.bOiiuk .chat-bubble-row .inline.full-width.full-height")
            if len(div_elms) > 0:
                for div_elm in div_elms:
                    result = {}
                    if len(p_elms) > 0:
                        last_date = getDateTime(p_elms[0].text)
                    result['Message'] = div_elm.text
                    result['Date'] = last_date
                    inner_outgoing_div = len(div_elm.find_elements_by_css_selector(".from-them"))
                    inner_call_div = len(div_elm.find_elements_by_css_selector(".is-call"))
                    # print(inner_outgoing_div, inner_call_div)
                    if inner_outgoing_div and not inner_call_div:
                        result['direction'] = "OUTGOING_TEXT"
                        self.outgoing = self.outgoing + 1
                    elif not inner_outgoing_div and not inner_call_div:
                        result['direction'] = "INCOMING_TEXT"
                        self.incoming = self.incoming + 1
                    elif inner_outgoing_div and inner_call_div:
                        result['direction'] = "OUTGOING_CALL"
                        self.outgoing = self.outgoing + 1
                    else:
                        result['direction'] = "INCOMING_CALL"
                        self.incoming = self.incoming + 1
                    results.append(result)
        # print(results)
        return results

    def checkDelete(self, pattern=None, target=None):
        # check if delete or not
        if not self.flag_delete:
            if pattern and target:
                self.flag_delete = (pattern == target)
            if self.position > self.delete_start_position:
                self.flag_delete = True

    def deleteConversation(self):
        if self.driver is None or not self.flag_delete: return False
        # archive span click
        try:
            archive_elm = self.driver.find_element_by_xpath('//span[text()="Archive"]')
            self.driver.execute_script("arguments[0].click();", archive_elm)
            time.sleep(3)
            button_elm = self.driver.find_element_by_xpath('//button[text()="Archive"]')
            close_elm = self.driver.find_elements_by_css_selector('.SpModalCloseIcon.sc-cFlXAS.hhjawh')
            if button_elm.is_displayed():
                self.driver.execute_script("arguments[0].click();", button_elm)
                time.sleep(5)
                return True
            if len(close_elm) > 0:
                self.driver.execute_script("arguments[0].click();", close_elm[0])
                time.sleep(5)
                return True
        except Exception as e:
            print("Exception in delete {}".format(e))
        return False

    def createLogFile(self):
        if self.file is not None: return
        filename = "logs/" + today_datetime + ".txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except:
                print("Exception in create new file")
        self.file = open(filename, "a")
    
    def closeLogFile(self):
        if self.file is None: return
        if self.flag_write:
            self.file.write("]")
        self.file.close()

    def readLogFile(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except:
            data = None
            print("Exception in read log {} file".format(f.name))
        return data

    def writeLogFile(self, data):
        if self.file is None: return
        try:
            if self.flag_write:
                self.file.write(",\n")
            else:
                self.flag_write = True
                self.file.write("[")
            json.dump(data, self.file)
        except:
            print("Exception in write log {} file".format(self.file.name))

    def post_request(self, data):
        request = requests.post(self.post_url, json=data, timeout=30)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}.".format(request.status_code))

    def run(self):
        try:
            self.createLogFile()
            self.openBrowser()
            self.login()
            while (self.position < self.max_total_count):
                self.clickItem()
                self.scrollDown()
        except Exception as e:
            print(e)
        finally:
            self.closeBrowser()
            self.closeLogFile()



if __name__ == "__main__":
    handler = SuperphoneScrapeConversations()
    handler.run()
