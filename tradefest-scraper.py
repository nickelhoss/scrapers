from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url = 'https://tradefest.io/en/search?lng=-95.712891&lat=37.09024&loc=United%20States&locType=country'

options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage')
#options.add_argument('--headless')
driver = webdriver.Chrome('/Users/nickgreen/Documents/Sites/chromedriver/chromedriver', options=options)
driver.get(url)

conference_list_window = driver.window_handles[0]
url_list = []

while True:
    try:
        more_info_buttons = driver.find_elements_by_link_text('More info')
        next_button_click = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Next")))

        for button in more_info_buttons:
            driver.execute_script("arguments[0].click()", button)
            conference_page_window = driver.window_handles[1]
            driver.switch_to.window(conference_page_window)
            try:
                conference_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Visit website"))).get_attribute('href')
                conference_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/main/app-event/div[1]/div/div/div/h1'))).text
                conference_location = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/mat-sidenav-container/mat-sidenav-content/main/app-event/app-event-overview/div/div/p[1]/span | /html/body/app-root/mat-sidenav-container/mat-sidenav-content/main/app-event/app-event-overview/div/div/p[1]/a[contains(@class, 'accent-link-g ng-star-inserted')]"))).text
                conference_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/main/app-event/div[1]/div/div/div/span'))).text
                url_list.append([conference_page, conference_name, conference_location, conference_date])
            except Exception as ex:
                print('Website link missing from from page')

            driver.close()
            driver.switch_to.window(conference_list_window)

        driver.execute_script("arguments[0].click()", next_button_click)
        time.sleep(2)

    except:
        print('...what happened?')
        break

url_list_df = pd.DataFrame(url_list, columns = ['url','name', 'conference_location','date'])
url_list_df.to_csv('tradefest.csv')
print(len(url_list_df))
print(url_list_df)
driver.quit()
