from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()
    print("clear button clicked.")

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


def clear_cookies(driver):
    driver.get("about:blank")
    
    # clear one function
    driver.delete_all_cookies()
    
    driver.execute_script('localStorage.clear();')


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


def main():
    chrome_options = build_chrome_options()
    driver = webdriver.Chrome(executable_path="D:/Development Tools/Python & Django/Selenium/chromedriver.exe", chrome_options=chrome_options)
    clear_cache(driver)
    clear_cookies(driver)
    time.sleep(5)
    driver.quit()




if __name__ == "__main__":
    main()