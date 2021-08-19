from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
import json
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['goods']
coll = db.mvideo

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get("https://mvideo.ru")

popup = driver.find_element_by_xpath (f"//span[@class='c-btn_close font-icon icon-delete']")
if (popup):
    popup.click()

block = driver.find_element_by_xpath(f"//h2[contains(text(),'Новинки')]/ancestor::div[@class='section']")

action = ActionChains(driver)
action.move_to_element(block)
action.perform()

time.sleep(2)

button = block.find_element_by_xpath(f".//a[contains(@class,'next-btn')]")
#print(button.get_attribute("class").split())
while 'disabled' not in button.get_attribute("class").split():
    button.click()
    time.sleep(3)

items = block.find_elements_by_xpath(f".//a[@data-product-info]")[::2]
for i in items:
    #print(i.get_attribute('data-product-info'))
    j = json.loads(i.get_attribute('data-product-info'))
    data = dict()
    data['_id'] = j['productId']
    data['name'] = j['productName']
    data['price'] = j['productPriceLocal']
    data['vendor'] = j['productVendorName']
    data['category'] = j['productCategoryName']
    #pprint(data)
    coll.update_one({'_id': data['_id']}, {'$set': data}, upsert=True)

driver.close()


