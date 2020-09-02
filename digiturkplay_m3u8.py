#!/usr/bin python3

from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from datetime import datetime, timezone, timedelta
import os
import json
import sys
import mysql.connector
# from pyvirtualdisplay import Display
import requests



class Digiturkplay:
    '''
    Digiturkplay Scrape and Get .m3u8
    '''
    base_url = "https://www.digiturkplay.com/"
    login_url = base_url + "kullanici/giris?r=%2Fkullanici%2Fgiris"
    list_url = base_url + "ulusal/masterchef-turkiye"
    REQUEST_TIME_OUT = 300

    # initialize
    def __init__(self, email="bahriinceler@hotmail.com", password="2334323a1"):
        self.driver = None
        self.email = email
        self.password = password
        self.open_browser = False
        self.log_print = True
        self.log_filename = "digiturkplay_log.txt"
        self.log_file = None
        self.is_checkable = True
        self.result = False
        self.str_result = ""
        self.m3u8_urls = []
        self.filters = None
        self.filepath = None
        self.download_url = None
        self.target_url_pattern = '.m3u8'
        self.target_url = None
        self.host=None,
        self.port=None,
        self.user=None,
        self.passwd=None,
        self.database=None,
        self.table=None,
        self.row_id = None

    # set parameters by argvs from command line
    def set_params(self, argvs):
        if (len(argvs) > 1):
            for argv in argvs:
                words = argv.split("=",1)
                if len(words) > 1:
                    key = words[0]
                    val = words[1]
                    setattr(self, key, val) 
        # filters
        if self.filters is not None:
            self.filters = self.filters.split(",")

    # open browser and log file
    def openBrowser(self):
        # open fake display
        # display = Display(visible=0, size=(800, 600))
        # display.start()

        # DesiredCapabilities
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}

        # chrome options
        chrome_options = webdriver.ChromeOptions()
        if self.open_browser :
            chrome_options.add_argument("--start-maximized")
        else :
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument("--disable-dev-shm-usage")
            # chrome_options.add_argument("--remote-debugging-port=9222")
        # chrome_options.add_argument("user-data-dir=user_data")

        # chrome self.driver
        self.driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options, desired_capabilities=caps)
        # self.driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options, desired_capabilities=caps)
        self.driver.get(self.login_url)

        try:
            self.log_file = open(self.log_filename, 'w')
        except:
            self.log_file = None
        time.sleep(10)

    # login
    def login(self):
        if self.driver is None: return
        self.write_log("login")

        try:
            self.driver.find_element_by_id("Email").send_keys(self.email)
            time.sleep(1)
            self.driver.find_element_by_id("Password").send_keys(self.password)
            time.sleep(2)
            
            # submit
            btn_login = self.driver.find_element_by_css_selector("form#form-login button")
            self.driver.execute_script("arguments[0].click();", btn_login)
            time.sleep(10)

            self.pass_block_side()
        except Exception as e:
            self.write_log(e)

    # pass block side
    def pass_block_side(self):
        if self.driver is None: return
        self.write_log("pass block site_helper")

        try:
            helper = self.driver.find_element_by_css_selector("div#site_helper")
            actionchains = ActionChains(self.driver) # initialize ActionChain object
            if helper.is_enabled and helper.is_displayed:
                closeButton = helper.find_element_by_css_selector("a#close")
                actionchains.move_to_element(closeButton)
                actionchains.click(closeButton)
                actionchains.perform()
                time.sleep(5)

        except Exception as e:
            self.write_log(e)

    # check login
    def check_login(self):
        if self.driver is None: return False

        try:
            to_main = self.driver.find_element_by_class_name("ga-ab-main")
            if to_main.get_attribute("id") == "login-link":
                return False
            if "profil" in to_main.get_attribute("href"):
                self.write_log("[checking login] with login status")
                return True

        except Exception as e:
            self.write_log(e)

        self.write_log("[checking login] without login status")
        return False

    # open list page
    def open_list_page(self):
        if self.driver is None: return
        self.write_log("open list page")

        try:
            self.driver.get(self.list_url)
            time.sleep(10)
            self.check_login()
            
            self.pass_block_side()
        except Exception as e:
            self.write_log(e)

    # find target
    def find_open_target(self):
        if self.driver is None: return
        self.write_log("find and open target video")

        try:
            time.sleep(10)
            items = self.driver.find_elements_by_css_selector("div.episode-container .episode-item")
            self.write_log("episode items {}".format(len(items)))

            max_episode_no = 0
            a_target_elm = None
            target_href_elm = None

            for item in items:
                class_value = item.get_attribute("class")
                episode_no = item.find_element_by_css_selector("span.episode-no")
                
                if episode_no:
                    no_value = episode_no.text.strip()
                    try:
                        no_value = int(no_value)
                    except:
                        no_value = 0

                    if no_value > max_episode_no:
                        max_episode_no = no_value

                        has_active = "active" in class_value.split()
                        
                        if not has_active:
                            # click target
                            self.driver.execute_script("arguments[0].click();", item)
                            time.sleep(2)
                        
                        a_target = item.find_element_by_css_selector("a.watch-button")
                        a_target_elm = a_target
                        target_href = a_target.get_attribute("href")
                        target_href_elm = target_href

            if a_target_elm is not None and target_href_elm is not None:
                self.write_log("target url is {}".format(target_href_elm))
                # open target video
                self.driver.execute_script("arguments[0].click();", a_target_elm)
                # self.get_desired_capabilities("find_open_target")
                time.sleep(10)
                self.check_login()

                return True

        except Exception as e:
            self.write_log(e)

        return False

    # confrim modal to play video
    def confirm_modal(self):
        if self.driver is None: return
        self.write_log("confirm modal to play video")

        try:
            modal = self.driver.find_element_by_css_selector("div#form-resumeplay")
            if modal.is_enabled and modal.is_displayed:
                confirmButton = modal.find_element_by_css_selector(".two-buttons a")
                # confirmButton.click()
                self.driver.execute_script("arguments[0].click();", confirmButton)
                # self.get_desired_capabilities("confirm_modal")
                self.write_log("no-continue button clicked")
                time.sleep(5)

        except Exception as e:
            self.write_log(e)
 
    # get .m3u8
    def get_m3u8(self):
        if self.driver is None: return

        try:
            self.get_desired_capabilities("get_m3u8 first")
            time.sleep(10)
            # self.get_desired_capabilities("get_m3u8 second")
        except Exception as e:
            self.write_log(e)

    # close browser and file
    def closeBrowser(self):
        if self.driver is None: return

        self.driver.quit()
        if self.log_file:
            self.log_file.close()

    # write log message
    def write_log(self, msg):
        if self.log_print:
            print(msg)

    # write log file
    def write_log_file(self, msg):
        try:
            self.write_log("write log file")
            self.str_result = self.str_result + str(msg)
            if self.log_file:
                self.log_file.write(str(msg))
        except Exception as e:
            self.write_log(e)

    # save all requests in log file
    def check_all_requests(self, tag=""):
        if self.driver is None or not self.is_checkable: return

        self.write_log("[{}] check all requests and save log file".format(tag))
        try:
            cnt_req = 0
            for request in self.driver.requests:
                cnt_req = cnt_req + 1

                if request.response:
                    str_url = "{}".format(request.url)
                    str_body = "{}".format(request.response.body)
                    if '/{}'.format(self.target_url_pattern) in str_url:
                        # self.write_log_file({
                            # 'url' : str_url,
                            # 'status_code' : request.response.status_code,
                            # 'Content-Type' : request.response.headers['Content-Type'],
                            # 'body' : str_body
                        # })
                        self.target_url = str_url
                        self.write_log_file(str_body)
                        self.get_m3u8_url()
                        self.write_log("[{}] got m3u8 url".format(tag))

            self.write_log("[{}] total requests count is {}.".format(tag, cnt_req))

        except Exception as e:
            self.write_log(tag)
            self.write_log(e)

    # get .m3u8 url
    def get_m3u8_url(self):
        if self.str_result != "":
            self.write_log("get m3u8 url from string")
            patterns = self.str_result.split("\n")
            if len(patterns) < 2:
                patterns = self.str_result.split("\\n")
            # self.write_log(patterns)

            for word in patterns:
                # self.write_log(word)
                if len(word) > 5 and word[-5:].lower() == self.target_url_pattern:
                    self.m3u8_urls.append(word)
                    # self.write_log(self.m3u8_urls)
                    self.result = True

    # download m3u8 to filepath using filters
    def download(self):
        if self.filters is None or self.filepath is None or len(self.m3u8_urls) == 0 or not self.result: return
        self.write_log("run download command")
        self.write_log(self.m3u8_urls)

        download_filename = self.m3u8_urls[0]
        for f in self.filters:
            for url in self.m3u8_urls:
                f = f.strip()
                if f != "" and f in url:
                    download_filename = url
        
        subpath = self.target_url.split(self.target_url_pattern)[0]

        self.download_url = '{}{}'.format(subpath, download_filename)
        command = 'ffmpeg -i "{}" -c copy {}'.format(self.download_url, self.filepath)
        self.write_log(command)

        result_cmd = os.system(command)
        if result_cmd == 0 or True:
            self.write_log('ffmpeg success')

            self.run_mysql()
        else:
            self.write_log('ffmpeg failed.')

    # get responses using desired_capabilities
    def get_desired_capabilities(self, tag=""):
        if self.driver is None or not self.is_checkable: return
        self.write_log("[{}] get all responses using desired_capabilities".format(tag))

        try:
            browser_log = self.driver.get_log('performance') 
            events = [json.loads(entry['message'])['message'] for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            # results = []
            result_exist = False
            
            for event in events:
                try:
                    params = event['params']
                    response = params['response']
                    url = response['url']
                    # self.write_log("[{}] desired_capabilities url is {}".format(tag, url))
                    if '/{}'.format(self.target_url_pattern) in str(url):
                        # results.append(response)
                        self.target_url = str(url)
                        result_exist = True
                        self.write_log("[{}] desired_capabilities url {} has pattern {}".format(
                            tag, url, self.target_url_pattern))
                except:
                    pass
            
            if not result_exist:
                self.write_log("[{}] desired_capabilities urls have never pattern {}".format(tag, self.target_url_pattern))
        except Exception as e:
            self.write_log(e)

    # run all performance
    def run(self):
        try:
            self.openBrowser()
            self.login()
            self.open_list_page()
            if self.find_open_target():
                self.confirm_modal()
                self.get_m3u8()
                self.request_m3u8()
                self.download()

        except Exception as e:
            self.write_log(e)
        finally:
            self.closeBrowser()

    # connect and run sql query
    def run_mysql(self): 
        if not self.result: return

        self.write_log("mysql database connect")
        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                use_unicode=True,
                charset="utf8"
            )
            
            cursor = conn.cursor()

            if conn and cursor:
                qry = """UPDATE {} SET is_downloaded = '1', `source_url` = %s WHERE id = %s""".format(self.table)
                cursor.execute(qry, (self.download_url, self.row_id))
                conn.commit()
                self.write_log("mysql row updated")

                cursor.close()
                conn.close()

        except Exception as e:
            self.write_log(e)

    # request .m3u8
    def request_m3u8(self):
        if self.target_url is None: return

        self.write_log("request for m3u8")
        try:
            response = requests.get(self.target_url, timeout=self.REQUEST_TIME_OUT, verify=False)
            if response.status_code == 200:
                self.write_log(response.content)
                self.write_log_file(response.content)
                self.get_m3u8_url()
            else:
                raise Exception("request failed to run by returning code of {}.".format(response.status_code))
        except Exception as e:
            self.write_log(e)


if __name__ == "__main__":
    handler = Digiturkplay()
    handler.set_params(sys.argv)
    handler.run()
