from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
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

data = pd.read_excel(r'C:\Users\slava\PycharmProjects\pythonAvito\Secondary_stage1_batch2.xlsx')

# url = 'https://yandex.ru/maps/2/saint-petersburg/?from=mapframe&ll=30.229042%2C60.038763&mode=usermaps&source=mapframe&um=constructor%3AW0xwJQSUJPrPTeQXbOC2KQxLeGGe3cPF&utm_source=mapframe&z=11.52'
# driver.get(url)
# input_tab = driver.find_element(By.TAG_NAME, 'input')
# time.sleep(1)
for ind, item in enumerate(data['Location']):
        try:

                url = 'https://yandex.ru/maps/2/saint-petersburg/?from=mapframe&ll=30.229042%2C60.038763&mode=usermaps&source=mapframe&um=constructor%3AW0xwJQSUJPrPTeQXbOC2KQxLeGGe3cPF&utm_source=mapframe&z=11.52'
                driver.get(url)
                time.sleep(1)
                input_tab = driver.find_element(By.TAG_NAME, 'input')

                input_tab.send_keys(item)
                driver.find_element(By.XPATH, './/div[@class = "small-search-form-view__icon _type_search"]').click()

                actions = ActionChains(driver)
                el = driver.find_element(By.XPATH, './/div[@class = "map-placemark"]')
                actions.move_to_element(el).perform()
                time.sleep(1)
                # driver.move_to_element_with_offset(el, 10, -10).click()
                # driver.move_to_element_with_offset(el, 10, -10).click()
                # location = el.location
                # x, y = location['x'], location['y']
                # print(x,y)
                actions.move_by_offset(100, 100).click().perform()
                time.sleep(1)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div[@class = "popup__content"]')))
                info = driver.find_element(By.XPATH, './/div[@class = "popup__content"]')
                data.at[ind, 'District'] = info.text
                driver.find_element(By.XPATH, './/button[@class = "button _view_search _size_medium"]').click()

        except:
                data.at[ind, 'District'] = 'Not obtained'
                driver.find_element(By.XPATH, './/button[@class = "button _view_search _size_medium"]').click()

data.to_excel('secondary_stage1_batch2_distr.xlsx')
