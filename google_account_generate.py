from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import string


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=20):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')
    try:
        # wait for the button to appear
        wait = WebDriverWait(driver, timeout)
        wait.until(get_clear_browsing_button)

        # click the button to clear the cache
        get_clear_browsing_button(driver).click()
        print("clear button clicked.")

        # wait for the button to be gone before returning
        wait.until_not(get_clear_browsing_button)
    except:
        pass


def clear_cookies(driver):
    try:
        driver.get("about:blank")
        driver.delete_all_cookies()
        driver.execute_script('localStorage.clear();')
    except:
        pass


def build_chrome_options():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_untrusted_certs = True
    chrome_options.assume_untrusted_cert_issuer = True
    # chrome configuration
    # More: https://github.com/SeleniumHQ/docker-selenium/issues/89
    # And: https://github.com/SeleniumHQ/docker-selenium/issues/87
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

    return chrome_options 


# Printing funtion with 3 modes
# 1 : Normal message
# 2 : Information message
# 3 : Caution message
def msg(
        _option_,
        _message_
        ):
    if _option_ == 1:
        print('\x1b[0;32;40m> %s\x1b[0m' % _message_)
    elif _option_ == 2:
        print('\x1b[0;32;40m>\x1b[0m %s' % _message_)
    elif _option_ == 3:
        print('\n\x1b[0;32;40m[\x1b[0m%s\x1b[0;32;40m]\x1b[0m' % _message_)
    else:
        print('\n\x1b[0;31;40m[ERROR]\x1b[0m')


# Exiting function
def ext():
    msg(1,'Exiting...')
    sys.exit()


# Function used to randomize credentials
def randomize(
                _option_,
                _length_
            ):

    if _length_ > 0 :

        # Options:
        #       -p      for letters, numbers and symbols
        #       -l      for letters only
        #       -n      for numbers only
        #       -m      for month selection
        #       -d      for day selection
        #       -y      for year selection

        if _option_ == '-p':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
        elif _option_ == '-l':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif _option_ == '-n':
            string._characters_='1234567890'
        elif _option_ == '-m':
            string._characters_='JFMASOND'

        if _option_ == '-d':
            _generated_info_=random.randint(1,28)
        elif _option_ == '-y':
            _generated_info_=random.randint(1950,2000)
        else:
            _generated_info_=''
            for _counter_ in range(0,_length_) :
                _generated_info_= _generated_info_ + random.choice(string._characters_)

        return _generated_info_

    else:
        msg(3,'No valid length specified...')
        ext()


first_name, last_name, username, password = '', '', '', ''
flag_fixed = True


# Function used to generate the credential information
def generate_info(driver):
    global first_name, last_name, username, password, flag_fixed

    # Print message
    msg(1,'Generating credentials...')

    # First and last name
    _first_name_=randomize('-l',7) if first_name == '' else first_name
    if flag_fixed : first_name = _first_name_
    driver.find_element_by_xpath("//input[@id='firstName']").send_keys(_first_name_)
    time.sleep(1)

    _last_name_=randomize('-l',8) if last_name == '' else last_name
    if flag_fixed : last_name = _last_name_
    driver.find_element_by_xpath("//input[@id='lastName']").send_keys(_last_name_)
    msg(2,'\x1b[0;33;40mName:\x1b[0m %s %s' % (_first_name_,_last_name_))
    time.sleep(1)

    # Username
    _username_=randomize('-l',10) if username == '' else username
    if flag_fixed : username = _username_
    driver.find_element_by_xpath("//input[@id='username']").send_keys(_username_)
    msg(2,'\x1b[0;33;40mUsername:\x1b[0m %s' % _username_)
    time.sleep(1)

    # Password
    _password_=randomize('-p',16) if password == '' else password
    if flag_fixed : password = _password_
    driver.find_element_by_xpath("//input[@name='Passwd']").send_keys(_password_)
    msg(2,'\x1b[0;33;40mPassword:\x1b[0m %s' % _password_)
    time.sleep(1)

    # Password Confirm
    driver.find_element_by_xpath("//input[@name='ConfirmPasswd']").send_keys(_password_)
    msg(2,'\x1b[0;33;40mPassword:\x1b[0m %s' % _password_)
    time.sleep(3)

    # Next Button Click
    driver.find_element_by_id("accountDetailsNext").click()
    msg(2,'\x1b[0;33;40mClicked Next Button:\x1b[0m')
    time.sleep(5)

    try:
        # Next Button Click
        if not driver.find_element_by_id("phoneNumberId"):
            flag_success = True
    except:
        flag_success = True

    # # Date of birth
    # _month_=randomize('-m',1)
    # _day_=randomize('-d',1)
    # _year_=randomize('-y',1)
    # pyautogui.typewrite(_month_+'\t'+str(_day_)+'\t'+str(_year_)+'\t')
    # msg(2,'\x1b[0;33;40mDate of birth:\x1b[0m %s/%d/%d' % (_month_,_day_,_year_))

    # # Gender (set to 'Rather not say')
    # pyautogui.typewrite('R\t')
    # msg(2,'\x1b[0;33;40mGender:\x1b[0m Rather not say')

    # # Skip the rest
    # pyautogui.typewrite('\t\t\t\t\n')


flag_success = False


def main():
    chrome_options = build_chrome_options()
    while not flag_success:
        driver = webdriver.Chrome(executable_path="D:/Development Tools/Python & Django/Selenium/chromedriver.exe", chrome_options=chrome_options)
        driver.get("https://accounts.google.com/signup")
        time.sleep(1)
        generate_info(driver)
        time.sleep(5)
        if flag_success : break
        clear_cache(driver)
        clear_cookies(driver)
        time.sleep(10)
        driver.quit()


if __name__ == "__main__":
    main()