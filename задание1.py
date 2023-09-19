from bs4 import BeautifulSoup
from selenium import webdriver as wd
import time
from datetime import datetime
import pandas as pd
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = wd.Chrome()

url = 'https://afi-v-park.ru/plans/search/'
driver.get(url)
data_list = []
for _ in range(100):
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_DOWN)
    time.sleep(0.1)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

for tag in soup.find_all("div", {"class": "item"}):
    property_info = {}

    title_element = tag.find('div', class_='card-mini__title')
    if title_element:
        property_info['type'] = str(title_element.text.strip()).split(', ')[0]
        property_info['area'] = str(title_element.text.strip()).split(', ')[1].split()[0]

    param_items = tag.find('div', class_='card-mini__param')
    if param_items:
        property_info['number'] = param_items.find('div', class_='card-mini__param-item tn').text.strip()
        property_info['floor'] = param_items.find('div', class_='card-mini__param-item f').text.strip()
        property_info['building'] = param_items.find('div', class_='card-mini__param-item b').text.strip()

    # Получаем цену и скидку
    price_element = tag.find('div', class_='card-mini__param-item tc')
    if price_element:
        property_info['price'] = price_element.text.strip()

    discounted_price_element = tag.find('div', class_='card-mini__param-item tcd terms__offer__text')
    if discounted_price_element:
        property_info['discounted_price'] = discounted_price_element.text.strip()


    # Выводим информацию о текущей недвижимости
    if property_info != {}:
        property_info['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Добавляем запись в список
        data_list.append(property_info)

    # Создаем DataFrame из списка данных
    df = pd.DataFrame(data_list)

    # Сохраняем DataFrame в Excel-файл
    df.to_excel('недвижимость.xlsx', index=False)

driver.quit()


