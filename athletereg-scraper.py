from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url = 'https://www.bikereg.com/'

options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/Users/nickgreen/Documents/Sites/chromedriver/chromedriver', options=options)
driver.get(url)

conference_list_window = driver.window_handles[0]
registrant_limit_list = []

while True:
    try:
        event_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 'ctl00_FullWidthHero_EventHeader_hpEventName'))).text
        registrant_limit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_EventChoice_lblFieldLimit'))).text
        registrant_limit_list.append([event_name, registrant_limit])
    except Exception as ex:
        print('Someting is missing...')
        break

url_list_df = pd.DataFrame(registrant_limit_list, columns = ['Event Name','Registrant Limit'])
url_list_df.to_csv('bikereg.csv')
print(len(url_list_df))
print(url_list_df)
driver.quit()
