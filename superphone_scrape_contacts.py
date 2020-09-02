from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import pandas as pd
import time
import sys


# config
SITE_URL = 'https://app.superphone.io/'
SITE_LOGIN_URL = SITE_URL + 'login/'
SITE_MESSAGE_URL = SITE_URL + 'messages'
SITE_CONTACT_URL = SITE_URL + 'contacts'
USER_EMAIL = 'lancecoleman91@gmail.com'
USER_PASSWORD = 'wecandoit!'
CHROMEDRIVER_PATH = 'chromedriver.exe'


# chrome driver
driver = None

# pandas data
df = pd.DataFrame(columns=['Name', 'Gender', 'photo link', 'City', 'State', 'Tags', 'LAST CONTACTED', '$ SPENT', 'Email', 'Messaging', 'Mobile', 'Assigned', 'Address', 'Instagram', 'Twitter', 'Birthday', 'Industry', 'Notes', 'Number of Messages Incoming', 'Number of Messages Outgoing', 'Etc'])


# get attr from path
def get_info(path, attr=None):
    try:
        elms = driver.find_elements_by_xpath(path)
        if len(elms) > 0:
            results = []
            for elm in elms:
                if attr is None :
                    results.append(elm.text)
                else :
                    results.append(elm.get_attribute(attr))
            
            if len(results) == 1:
                return results[0]
            elif len(results) > 1:
                return results
    except Exception as e:
        print(e)
    return ""


# run chrome
def run_chrome():
    global driver

    try:
        # chrome driver
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=op)
        driver.maximize_window()

        # login
        driver.get(SITE_LOGIN_URL)
        time.sleep(10)
        driver.find_element_by_xpath("//input[@id='email']").send_keys(USER_EMAIL)
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='password']").send_keys(USER_PASSWORD)
        time.sleep(2)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(10)

        page = 0
        limit = 500
        row = 0
        while(True):
            path = "?&page={0}&limit={1}".format(page, limit)

            # open contact page
            driver.get(SITE_CONTACT_URL + path)
            time.sleep(10)

            trs = driver.find_elements_by_xpath("//tr[@class='with-highlight']")

            if len(trs) == 0: break

            # get all contacts
            for tr in trs:
                tr.click()
                time.sleep(5)

                # get all infos
                name            = get_info("//span[@class='SpContactName sc-gmeYpB bKDGrO']")
                photo_link      = get_info("//div[@class='thumbnail-wrapper circular lg']/img", "src")
                tags            = get_info("//div[@class='tags-list']/button")
                last_contacted  = get_info("//div[@class='stat'][1]/h3")
                spent           = get_info("//div[@class='stat'][2]/h3")
                keys            = get_info("//div[@class='sc-cNnxps cCzEKX']")
                
                gender          = None
                city            = None
                state           = None
                email           = None
                messaging       = None
                mobile          = None
                assigned        = None
                address         = None
                instagram       = None
                twitter         = None
                birthday        = None
                industry        = None
                notes           = None
                messages_incoming = None
                messages_outgoing = None
                etc             = None

                if len(keys) > 0:
                    i = 1
                    for key in keys:
                        try:
                            if key.lower() == "email" : email = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]/a".format(i))
                            elif key.lower() == "mobile" : mobile = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]/a".format(i))
                            elif key.lower() == "assigned" : assigned = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]".format(i))
                            elif key.lower() == "address" : 
                                address = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]".format(i))
                                address = address.split('\\n')[0]
                                city = address.split(',')[0]
                                state = address.split(',')[1]
                            elif key.lower() == "instagram" : instagram = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]/a".format(i))
                            elif key.lower() == "twitter" : twitter = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]/a".format(i))
                            elif key.lower() == "birthday" : birthday = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]".format(i))
                            elif key.lower() == "industry" : industry = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]".format(i))
                            elif key.lower() == "job title" : notes = get_info("//div[@class='sc-fAJaQT gNIPBu'][{}]/div[2]".format(i))
                        except Exception as e:
                            print(e)
                        i = i + 1

                df.loc[row] = [name, gender, photo_link, city, state, tags, last_contacted, spent, email, messaging, mobile, assigned, address, instagram, twitter, birthday, industry, notes, messages_incoming, messages_outgoing, etc]
                row = row + 1

            page = page + 1
            # if row > 10:
            #     df.to_excel('Sample1.xlsx', sheet_name='Sheet1')
            #     break

        # quit
        time.sleep(10)
        driver.quit()
    except Exception as e:
        print(e)

# main
def main():
    try:
        # run chrome
        run_chrome()

        # print result
        df.head(10)
        
    except Exception as e:
        print(e)

# call main
if __name__ == "__main__":
    main()