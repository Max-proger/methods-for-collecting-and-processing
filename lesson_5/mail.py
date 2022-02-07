import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

client = MongoClient("127.0.0.1", 27017)
db = client["mail_database"]
incoming_mail = db.incoming_mail
incoming_mail.drop()

mail = input("Введите вашу электронную почту: ")
password = input("Введите ваш пароль: ")
chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("__headless")
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)

driver.get("https://mail.ru/")

elem = driver.find_element(By.NAME, "login")
elem.send_keys(mail)
elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.NAME, "password")
elem.send_keys(password)
elem.send_keys(Keys.ENTER)

driver.get(driver.find_element(By.XPATH, '//div[contains(@role, "rowgroup")]/a[1]').get_attribute("href"))

while True:
    time.sleep(0.5)
    sender = driver.find_element(By.XPATH, '//div[@class="letter__author"]/span[1]').text
    date = driver.find_element(By.CLASS_NAME, "letter__date").text
    topic = driver.find_element(By.TAG_NAME, "h2").text
    content = (
        WebDriverWait(driver, 10)
        .until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'style_')]")))
        .get_attribute("innerHTML")
    )
    try:
        incoming_mail.insert_one({"sender": sender, "date": date, "topic": topic, "content": content})
    except:
        pass

    button = driver.find_element(By.XPATH, "//span[@data-title-shortcut = 'Ctrl+↓']")
    arrow_down = button.get_attribute("disabled")
    if arrow_down is not None:
        break
    button.click()
