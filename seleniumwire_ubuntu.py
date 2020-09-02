from seleniumwire import webdriver  # Import from seleniumwire

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--headless')
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument('--no-sandbox')

# Create a new instance of the Firefox driver
driver = webdriver.Chrome("/home/ceek/html/ceek2/chromedriver", chrome_options=chrome_options)

# Go to the Google home page
driver.get('https://www.google.com')

f = open('seleniumwire_log.txt', 'w')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(request, request.response)
        continue
        f.write(str({
            'url' : request.url,
            'status_code' : request.response.status_code,
            'Content-Type' : request.response.headers['Content-Type'],
            'body' : request.response.body
        }))

driver.quit()

f.close()
