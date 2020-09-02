from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.interaction import KEY
import pyautogui
import time
import sys
import random


class MultiTabsRefreshWebDriver:

    FLAG_FOREVER = True
    MAX_NUMBERS = 10
    TIME_NEXT = 0
    TIME_DELTA = 500
    IS_SHOW = True
    IMAGE_SHOW = False
    OS_TYPE = 'WINDOWS'
    # OS_TYPE = 'LINUX'

    def __init__(self, url, count_tabs=1, refresh_time=10, first_time=0, proxy='', useragent='', proxy_txt='', useragent_txt=''):
        self.url = url
        self.driver = None
        self.chrome_options = None
        self.flag_exit = False
        self.count_tabs = count_tabs
        self.refresh_time = refresh_time
        self.first_time = first_time
        self.count_requests = 0

        self.proxy_txt = proxy_txt
        if proxy == '' : 
            self.proxy = MultiTabsRefreshWebDriver.read_choice_text(proxy_txt)
        else:
            self.proxy = proxy # test with any ip address which supports `http` as well because the link within the script are of `http`
        
        self.headless = not MultiTabsRefreshWebDriver.IS_SHOW
        self.os_type = MultiTabsRefreshWebDriver.OS_TYPE
        self.image_show = MultiTabsRefreshWebDriver.IMAGE_SHOW
        self.extension_path = r"reload all tabs.crx"
        
        self.useragent_txt = useragent_txt
        if useragent == '' : 
            self.useragent = MultiTabsRefreshWebDriver.read_choice_text(useragent_txt)
        else:
            self.useragent = useragent
        
        # self.reload_method = 'JAVASCRIPT'
        self.reload_method = 'EXTENSION'


    @staticmethod
    def read_choice_text(filename):
        result = ''
        try:
            if filename != '':
                with open(filename, "r") as fp:
                    lines = fp.readlines()
                    result = random.choice(lines)
                    fp.close()
        except:
            pass
        return result


    def get_clear_browsing_button(self):
        """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
        return self.driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


    def clear_cache(self, timeout=20):
        """Clear the cookies and cache for the ChromeDriver instance."""
        # navigate to the settings page
        self.driver.get('chrome://settings/clearBrowserData')
        try:
            # wait for the button to appear
            wait = WebDriverWait(self.driver, timeout)
            wait.until(self.get_clear_browsing_button)

            # click the button to clear the cache
            self.get_clear_browsing_button().click()
            print("clear button clicked.")

            # wait for the button to be gone before returning
            wait.until_not(self.get_clear_browsing_button)
        except:
            pass


    def clear_cookies(self):
        try:
            # self.driver.get("about:blank")
            self.driver.delete_all_cookies()
            self.driver.execute_script('localStorage.clear();')
        except:
            pass


    def build_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.accept_untrusted_certs = True
        chrome_options.assume_untrusted_cert_issuer = True
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-impl-side-painting")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-seccomp-filter-sandbox")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-cast")
        chrome_options.add_argument("--disable-cast-streaming-hw-encoding")
        chrome_options.add_argument("--disable-cloud-import")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-session-crashed-bubble")
        chrome_options.add_argument("--disable-ipv6")
        chrome_options.add_argument("--allow-http-screen-capture")
        chrome_options.add_argument("--start-maximized")
        if self.headless :
            chrome_options.add_argument('--headless')
        if self.proxy != '':
            chrome_options.add_argument('--proxy-server={}'.format(self.proxy))
        if self.useragent != '':
            chrome_options.add_argument('--user-agent={}'.format(self.useragent))
        if self.extension_path :
            # chrome_options.add_argument("--incognito")
            chrome_options.add_extension(self.extension_path)
        if not self.image_show :
            prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
            chrome_options.add_experimental_option('prefs', prefs)

        self.chrome_options = chrome_options


    def check_exit(self):
        self.count_requests = self.count_requests + 1
        if MultiTabsRefreshWebDriver.FLAG_FOREVER :
            self.flag_exit = False
        elif self.count_requests >= MultiTabsRefreshWebDriver.MAX_NUMBERS :
            self.flag_exit = True
        else :
            self.flag_exit = False
        return self.flag_exit


    def refresh_all_tabs_javascript(self):
        # using javascript
        allTabs = self.driver.window_handles
        step_time = int(self.refresh_time * 1000)

        while not self.check_exit():
            current_time = int(time.time() * 1000)
            next_refresh_time = current_time + step_time - MultiTabsRefreshWebDriver.TIME_DELTA
            # print(current_time, next_refresh_time)

            self.clear_cookies()
            # self.clear_cache()
            
            script_content = """
                ref_time = {0}
                step_time = {1}
                function refresh() {{
                    cur_time = Date.now();
                    if(cur_time >= ref_time || Math.abs(cur_time - ref_time) {2} step_time < 5)
                        location.reload();
                    else
                        setTimeout(refresh, 5);
                }}
                setTimeout(refresh, 5);
                """.format(next_refresh_time, step_time, '%')
            # print(script_content)

            for tab in allTabs:
                self.driver.switch_to.window(tab)

                # self.driver.refresh()
                # self.driver.execute_script("location.reload();")

                # self.driver.execute_script("window.close();")

                self.driver.execute_script(script_content)

                if MultiTabsRefreshWebDriver.TIME_NEXT > 0:
                    time.sleep(MultiTabsRefreshWebDriver.TIME_NEXT)
            
            time.sleep(self.refresh_time)


    def refresh_all_tabs_extension(self):
        # using chrome extension
        while not self.check_exit():
            time.sleep(self.refresh_time)

            self.clear_cookies()
            # self.clear_cache()

            # action = ActionChains(self.driver)
            # action.key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys("r").key_up(Keys.SHIFT).key_up(Keys.ALT).perform()
            # action.context_click(self.driver.find_element_by_tag_name("body")).perform()
            # action.send_keys(Keys.ALT, Keys.SHIFT, "r").perform()
            # action.move_by_offset(0,0).click().perform()

            # pyautogui.typewrite(['down','down','down','down','down','down','down','down','enter'])
            pyautogui.hotkey('alt', 'shift', 'r')

            # self.driver.find_element_by_tag_name("html").send_keys(Keys.ALT, Keys.SHIFT, "r")
            # self.driver.find_element_by_tag_name("body").send_keys(Keys.F1)


    def run(self):
        try:
            # open browser
            self.build_chrome_options()
            if self.os_type == 'WINDOWS' :
                self.driver = webdriver.Chrome(executable_path="chromedriver.exe", options=self.chrome_options)
            elif self.os_type == 'LINUX' :
                # self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
                self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.chrome_options)

            # open tabs
            self.driver.get(self.url)
            time.sleep(self.first_time)
            for i in range(self.count_tabs-1):
                self.driver.execute_script("""
                    window.open('{}');
                    """.format(self.url))

            # refresh pages
            if self.reload_method == 'JAVASCRIPT' :
                self.refresh_all_tabs_javascript()
            elif self.reload_method == 'EXTENSION' :
                self.refresh_all_tabs_extension()

            # close
            # time.sleep(100)
            self.driver.quit()
        
        except Exception as e:
            print(e)


    @staticmethod
    def help():
        print("""
        You must input like below.
        python multi_tabs_refresh.py <url> <counter of tabs> <refresh time> <first wait time> <proxy text file> <user agent text file>
        python multi_tabs_refresh.py http://localhost/test/counter_requests.php 100 2.5 10 proxy.txt useragent.txt
        """)


def main():
    try:
        if len(sys.argv) > 6:
            # input site url
            url = sys.argv[1]
            # input counter of tabs
            cnt = int(sys.argv[2])
            # input refresh time
            ref_time = float(sys.argv[3])
            # input first wait time
            first_time = float(sys.argv[4])
            # input proxy text file
            proxy_txt = sys.argv[5]
            # input user agent text file
            useragent_txt = sys.argv[6]

            MultiTabsRefreshWebDriver(
                url=url,
                count_tabs=cnt,
                refresh_time=ref_time,
                first_time=first_time,
                proxy_txt=proxy_txt,
                useragent_txt=useragent_txt
            ).run()
        else:
            MultiTabsRefreshWebDriver.help()
    except:
        MultiTabsRefreshWebDriver.help()



if __name__ == "__main__":
    main()