from selenium import webdriver
# from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time
from selenium.webdriver.common.by import By
import pandas as pd
import random

# from proxy_auth_data import login, password

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
# options.add_argument(('--headless'))
# options.add_argument('--proxy-server=45.94.228.253:8000')
# proxy_options = {
#         'proxy': {
#                 'https': f'http://{login}:{password}@45.94.228.253:8000'
#         }
#}
# driver = webdriver.Chrome(seleniumwire_options = proxy_options)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options = options)

stealth(driver,
        languages = ['en-US', 'en', 'ru'],
        vendor = 'Google Inc.',
        platform = 'Win32',
        webgl_vendor = 'Intel Inc.',
        renderer = 'Intel Iris OpeGL Engine',
        fix_hairline = True)

url = 'https://www.avito.ru/sankt-peterburg/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?f=ASgBAQICAUSSA8YQAkDmBxSMUsoIJIRZglk&p=2'
driver.get(url)
time.sleep(3)

for p in range(21):
        url = driver.current_url
        driver.get(url)
        time.sleep(3)
        items = driver.find_elements(By.XPATH, './/div[@data-marker = "item"]')
        df = pd.DataFrame(columns=['Price', 'Title', 'Description', 'Location', 'Metro', 'House_info'])

        for index, item in enumerate(items):
                try:
                        actions = ActionChains(driver)
                        actions.move_to_element(item).perform()
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(item)).click()
                        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(random.randint(2, 6))

                        price = driver.find_element(By.XPATH,
                                                    './/span[@class = "js-item-price style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI"]')
                        title =  driver.find_element(By.XPATH,
                                                     './/span[@class = "title-info-title-text"]')
                        description = driver.find_element(By.XPATH, './/ul[@class="params-paramsList-zLpAu"]')

                        location = driver.find_element(By.XPATH, './/span[@class="style-item-address__string-wt61A"]')

                        try:
                                metro = driver.find_element(By.XPATH, './/span[@class="style-item-address-georeferences-item-TZsrp"]').text
                        except:
                                metro = 'Not stated'

                        house_info = driver.find_element(By.XPATH, './/div[@class="style-item-params-McqZq"]')

                        df.at[index, 'Price'] = price.text
                        df.at[index, 'Title'] = title.text
                        df.at[index, 'Description'] = description.text
                        df.at[index, 'Location'] = location.text
                        df.at[index, 'Metro'] = metro
                        df.at[index, 'House_info'] = house_info.text

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                except:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

        with pd.ExcelWriter('Вторичка_234 _2.xlsx', mode = 'a', engine= 'openpyxl',
                            if_sheet_exists = 'overlay') as writer: df.to_excel(writer,
                                                                                sheet_name = 'Sheet1', startrow = writer.sheets['Sheet1'].max_row,
                                                                                header = None)
        time.sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.XPATH, '//span[@data-marker = "pagination-button/next"]'))).click()
# driver.quit()
