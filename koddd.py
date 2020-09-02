from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.common.by import By
import json
import time
from selenium.webdriver.firefox.options import Options
import sys
import psutil
import pymysql
import multiprocessing
import urllib.parse

def getM3U8():
	if len(sys.argv) < 2:
		print('Normal usage: python file.py <filename-containing-urls-with-extension>')
		print('To insert .m3u8 url to mysql database: python file.py <filename-containing-urls-with-extension> sql')
		sys.exit(1)

	sqlFlagOkay = 0
	if len(sys.argv) == 3:
		sqlFlagOkay = 1

	# opening urls file containing id value and url seperated by comma
	'''
		101,https://facebook.com
		102,https://twitter.com
	'''
	url = [] # takes second value from the file
	idd = [] # takes first value from the file 
	z = open(sys.argv[1])

	keywords = []
	for x in z:
		line = x.rstrip().strip().split(",")
		idd.append(line[0])
		url.append(line[1])
		keys = line[2].split(":")
		if len(keys) > 1:
  			keys.remove('')
		keywords.append(keys)
	z.close()

	options = Options()
	options.headless = True

	# Change below line to match your folder
	dic={'port':8090}
	server = Server("browsermob-proxy/browsermob-dist/src/main/scripts/browsermob-proxy",options=dic)
	server.start()
	proxy = server.create_proxy({'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})
	profile = webdriver.FirefoxProfile()
	profile.set_proxy(proxy.selenium_proxy())
	driver = webdriver.Firefox(firefox_profile=profile,options=options)

	for j in range(len(url)):
		print('Started time :',time.time())
		if sqlFlagOkay == 1:
			sqlFlag = 1
		else:
			sqlFlag = 0

		filename = str(int(time.time()))
		try:
			proxy.new_har('test')
			driver.get(url[j])

			'''
			#################################################
			Below Function:  Waits for the network to be quiet

			Parameters:	
			quiet_period (int) – number of milliseconds the network needs to be quiet for
			timeout (int) – max number of milliseconds to wait
			'''

			proxy.wait_for_traffic_to_stop(1,180)

			# adds a 20 second delay 
			time.sleep(30)

			driver.save_screenshot(filename+'_screenshot.png')
			f = open(filename+'_log.csv','w')
			for ent in proxy.har['log']['entries']:
				link = ent['request']['url']
				f.write(link)
				f.write("\n")
				if ".m3u8" in link:
					if (link[-4:] == "m3u8" or ".m3u8?" in link) and (("%" not in link) or ("//" not in link and "%" in link and ".m3u8" in link)) and any(keyword in link for keyword in keywords[j]): 
						link = urllib.parse.unquote(link)
						print(link)
						if sqlFlag == 1:
							try:
								# Change the below line to match your setup, also change to idd (id) value in line after that
								db = pymysql.connect(host='127.0.0.1', port=7999, user='bahri', passwd='Selamsana5.5', db='xtream_iptvpro',autocommit=True)
								cur = db.cursor()
								stream_source = link.replace("yayin2","boss")
								stream_source = stream_source.replace("foxtv_480p","foxtv_720p")
								stream_source = stream_source.replace("index_550","index_1250")
								stream_source = stream_source.replace("index_650_av-p","index_1550_av-p")
								stream_source = stream_source.replace("haberturk/playlist","haberturk/haberturk_720p")
								sqlQuery = "UPDATE streams SET stream_source='[\""+stream_source+"\"]' WHERE id=" + str(idd[j])
								# print(sqlQuery)
								cur.execute(sqlQuery)
								db.close()
								sqlFlag = 0
								break
							except Exception as e:
								print("****MYSQL***** Exeception occured : {} and here is the MYSQL Query : {}".format(e,sqlQuery))
						break
			print('Ended time :',time.time())
			f.close()
		except Exception as e:
			print("**Expection***",e)
	driver.quit()
	server.stop()

if __name__ == '__main__':

	for proc in psutil.process_iter():
		# check whether the process name matches
		if proc.name() == "browsermob-proxy":
			proc.kill()
		if proc.name() == "browsermob":
			proc.kill()
		if proc.name() == "firefox":
			proc.kill()
		if proc.name() == "java":
			proc.kill()

	# calling our scarping function
	getM3U8()

	for proc in psutil.process_iter():
		# check whether the process name matches
		if proc.name() == "browsermob-proxy":
			proc.kill()
		if proc.name() == "browsermob":
			proc.kill()
		if proc.name() == "firefox":
			proc.kill()
		if proc.name() == "java":
			proc.kill()

