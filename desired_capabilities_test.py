import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')


caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}

# driver = webdriver.Chrome(desired_capabilities=caps)
driver = webdriver.Chrome(service_args=["--verbose", "--log-path=desired_selenium.log"], desired_capabilities=caps, options=chrome_options)
driver.get('https://stackoverflow.com/questions/52633697/selenium-python-how-to-capture-network-traffics-response')

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    # response = json.loads(entry['message'])
    return response

browser_log = driver.get_log('performance') 

# print(browser_log)

events = [process_browser_log_entry(entry) for entry in browser_log]
events = [event for event in events if 'Network.response' in event['method']]

# print(events)

urls = []
target_url_pattern = 'ivc'
results = []
for event in events:
    try:
        params = event['params']
        response = params['response']
        url = response['url']
        urls.append(url)
        if target_url_pattern in str(url):
            results.append(response)
    except:
        pass

print(results)

with open('desired_selenium.txt', 'w') as outfile:
    # json.dump(events, outfile)
    json.dump(urls, outfile)

driver.quit()