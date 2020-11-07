import selenium
import json
import requests
import pandas as pd
import re

pd.options.display.max_rows = None
#pd.options.display.max_columns = None
#pd.options.display.max_colwidth = None

from bs4 import BeautifulSoup
from datetime import datetime
from selenium.common.exceptions import TimeoutException

#firefoxOptions = Options()
#firefoxOptions.add_argument('-headless')

doctorRes = {}
scheduleRes = {}
titleList = []
cityList = []
urlList = []

# list for doctor name list
doctorNameList = []
doctorSpecList = []
urlProfileList = []
profileDetailRes = {}

#webDriverPath = '/opt/firefox/geckodriver/geckodriver'
baseUrl = 'https://www.doctor360.com.au'
#driver = webdriver.Firefox(executable_path=webDriverPath, options=firefoxOptions)
#driver.implicitly_wait(10)
#wait = WebDriverWait(driver,10)
#headers = {'User-Agent': driver.execute_script('return navigator.userAgent;')}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# first layer page, get main page
firstLayerPage = requests.get(baseUrl, headers = headers)
soup = BeautifulSoup(firstLayerPage.content, 'html.parser')

for li in soup.findAll('div', class_='text-left col-md-2 col-sm-4 col-xs-6'):
	# get category
	title = li.find('h4')
	#print(title.text)
	for cat in li.findAll('a'):
		# get city
		splittedText = cat.text.split(' ')
		city = splittedText[-1]
		#doctorProfileRes.update({'city', city})
		#print(city[-1])

		# get url to second layer
		layerTwoUrl = cat['href']
		#print(cat['href'])

		# second layer page, get list of doctor for each category and city
		try:
			secondLayerUrl = baseUrl + layerTwoUrl
			secondLayerPage = requests.get(secondLayerUrl, headers = headers)
	
			soup = BeautifulSoup(secondLayerPage.content, 'html.parser')
			matchText = soup.findAll('span', class_='matches-found-text')

			if len(matchText) == 2:
				splittedText = matchText[1].text.split(' ')
				numOfPage = splittedText[7]
				#print(numOfPage)

				# get list of doctor for every page on second layer page
				for i in range(1, int(numOfPage) + 1):
					try:
						targetUrl = secondLayerUrl + '?page=' + str(i)

						secondLayerPage = requests.get(targetUrl, headers = headers)
						#print(targetUrl)
						soup = BeautifulSoup(secondLayerPage.content, 'html.parser')
						#titles = soup.findAll('span', class_='col-md12 col-xs-12 col-sm-12 title')
						titles = soup.findAll('div', class_='col-md-12 col-xs-12 col-sm-12 title')
						#print(len(titles))			
						
						for title in titles:
							doctorProfileRes = {}
							# get doctor name
							doctorName = title.find('h2')
							doctorNameList.append(doctorName.text)
							#doctorProfileRes.update({'name' : doctorName.text})
							#print(doctorName.text)

							# get doctor specialty
							doctorSpec = title.find('h3')
							doctorSpecList.append(doctorSpec.text)
							#doctorProfileRes.update({'specialty' : doctorSpec.text})
							#print(doctorSpec.text)

							# get url to profile page
							profileUrl = title.find('a')
							urlProfileList.append(str(profileUrl['href']))
							layerThreeUrl = profileUrl['href']
							#print(profileUrl['href'])
							#print('--------------')

							# third layer page, get profile detail for each doctor
							try:
								#clinicRes = {}
								
								thirdLayerUrl = baseUrl + layerThreeUrl
								thirdLayerPage = requests.get(thirdLayerUrl, headers = headers)

								soup = BeautifulSoup(thirdLayerPage.content, 'html.parser')
								#profileDetails = soup.findAll('div', class_='col-md-12 col-lg-12 col-sm-12 info_block')

								# get profile & clinic detail
								doctorRes[doctorName.text] = {}
								profileDetail = {}								
								scheduleDetail = {}

								for detail in soup.find('div', class_='col-md-12 col-lg-12 col-sm-12 info_block'):
									tdList = detail.findAll('td')

									for td in tdList:
										if (tdList.index(td) % 2) == 0:
											key = tdList[tdList.index(td)].text.rstrip().replace(':', '')
											profileDetail[key] = tdList[tdList.index(td)+1].text
														
								doctorRes[doctorName.text]['profileDetail'] = profileDetail
								#print(profileDetail)
								#print('------------------------------------------')

								for schedule in soup.find('table', class_='table table-bordered working-hours'):
									trList = schedule.findAll('tr')

									for tr in trList:
										tdList = tr.findAll('td')

										for td in tdList:											

											if tdList.index(td) == 0:												
												scheduleDetail[tdList[tdList.index(td)].text] = {}
												scheduleDetail[tdList[tdList.index(td)].text]['Morning'] = tdList[tdList.index(td)+1].text
												scheduleDetail[tdList[tdList.index(td)].text]['Evening'] = tdList[tdList.index(td)+2].text
											
								doctorRes[doctorName.text]['schedule'] = scheduleDetail
								#print(scheduleDetail)
								#print('------------------------------------------')
																
							except TimeoutException as ex:
								print('Timeout')

					except TimeoutException as ex:
						print('Timeout')				
			else:
				pass			
		except TimeoutException as ex:
			print('Timeout')

doctorRes = json.dumps(doctorRes)
print(doctorRes)
