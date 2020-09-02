from seleniumwire import webdriver  # Import from seleniumwire

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')

# Create a new instance of the Firefox driver
driver = webdriver.Chrome("chromedriver", options=chrome_options)

# Go to the Google home page
driver.get('https://www.google.com')

f = open('seleniumwire_log.txt', 'w')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        f.write(str({
            'url' : request.url,
            'status_code' : request.response.status_code,
            'Content-Type' : request.response.headers['Content-Type'],
            'body' : request.response.body
        }))

driver.quit()

f.close()