from datetime import datetime
from time import sleep
from sys import argv

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

options = webdriver.FirefoxOptions()
options.headless = True
for option in argv:
    if option == "--full":
        print("Opening without headless mode")
        options.headless = False
adblocker_path = r'C:\Users\user\PycharmProjects\LiraRate\extensions\adblock_plus.xpi'


def to_number(num):
    number = ""
    for digit in num:
        if digit != ",":
            number += digit
    return float(number)


def open_editor():
    browser.find_element_by_xpath(
        '//*[@id="elementor-panel-footer-navigator"]').click()
    browser.find_element_by_xpath(
        '//*[@id="elementor-navigator__elements"]/div/div/div[1]/div[1]/div[1]/i').click()
    browser.find_element_by_xpath(
        '//*[@id="elementor-navigator__elements"]/div/div/div[1]/div[2]/div/div[1]/div[1]/i').click()
    browser.find_element_by_xpath(
        '//*[@id="elementor-navigator__elements"]/div/div/div[1]/div[2]/div/div[2]/div/div[1]').click()
    browser.find_element_by_xpath(
        '//*[@id="elementor-controls"]/div[2]/div/div/div/pre/div[2]/div').click()


def change_script_tags(text):
    ActionChains(browser) \
        .key_down(Keys.CONTROL) \
        .send_keys("A") \
        .key_up(Keys.CONTROL) \
        .send_keys(Keys.DELETE) \
        .send_keys(text) \
        .key_down(Keys.CONTROL) \
        .key_down(Keys.SHIFT) \
        .send_keys(Keys.END) \
        .key_up(Keys.SHIFT) \
        .key_up(Keys.CONTROL) \
        .send_keys(Keys.DELETE) \
        .perform()
    browser.find_element_by_xpath(
        '//*[@id="elementor-panel-saver-button-publish"]').click()
    sleep(15)


username = r'dailylira'
password = r'Willokiki11??'
prices_url = r"https://lirarate.org"
metals_url = r"https://goldprice.org"
lira_editor = r"https://dailylira.com/wp-admin/post.php?post=2&action=elementor"
gold_editor = r"https://dailylira.com/wp-admin/post.php?post=17&action=elementor"
silver_editor = r"https://dailylira.com/wp-admin/post.php?post=23&action=elementor"

print("Starting Browser")
browser = webdriver.Firefox(options=options)
browser.install_addon(adblocker_path, temporary=True)
browser.profile = webdriver.FirefoxProfile()
browser.profile.add_extension(adblocker_path)
print("Getting prices")

browser.switch_to.window(browser.window_handles[0])
browser.get(prices_url)
sleep(10)
dollar_buy_rate = browser.find_element_by_xpath(
    '//*[@id="latest-buy"]').text
dollar_sell_rate = browser.find_element_by_xpath(
    '//*[@id="latest-sell"]').text
print("Found Buy & Sell prices")
dollar_buy_rate = to_number(dollar_buy_rate.split()[-2])
dollar_sell_rate = to_number(dollar_sell_rate.split()[-2])

print(f"Buy Price: {dollar_buy_rate} & Sell Price: {dollar_sell_rate}")
sleep(3)

print("Getting metal prices")
browser.get(metals_url)
sleep(5)
gold_price = to_number(browser.find_element_by_xpath(
    '//*[@id="gpxtickerLeft_price"]').text)
silver_price = to_number(browser.find_element_by_xpath(
    '//*[@id="gpxtickerMiddle_price"]').text)
print(f"Gold Price: {gold_price} & Silver Price: {silver_price}")

now = datetime.now()
hour = now.hour
date = f"{now.day}-{now.month}-{now.year}"
time_format = "AM"
if now.hour > 12:
    hour = now.hour - 12
    time_format = "PM"
elif now.hour == 0:
    hour = 12
minutes = now.minute
if now.minute < 10:
    minutes = f"0{minutes}"
current_time = f"{hour}:{minutes} {time_format}, {date}"
print(current_time)

with open("liraContent.txt", "r") as f:
    lira_content = ''
    for line in f:
        temp_line = ''
        for char in line:
            if char == "#":
                char = f"{dollar_buy_rate}"
            elif char == "^":
                char = f"{dollar_sell_rate}"
            elif char == "~":
                char = f'"{current_time}"'
            elif char == "*":
                char = f'{datetime.utcnow().minute}'
            elif char == "$":
                char = f'{datetime.utcnow().hour}'
            elif char == "@":
                char = f'{datetime.utcnow().second}'
            elif char == "&":
                char = f'{datetime.utcnow().day}'
            temp_line += char
        lira_content += temp_line
print(lira_content)

with open("silverContent.txt", "r") as f:
    silver_content = ''
    for line in f:
        temp_line = ''
        for char in line:
            if char == "#":
                char = f"{silver_price}"
            elif char == "~":
                char = f'"{current_time}"'
            elif char == "*":
                char = f'{datetime.utcnow().minute}'
            elif char == "$":
                char = f'{datetime.utcnow().hour}'
            elif char == "@":
                char = f'{datetime.utcnow().second}'
            elif char == "&":
                char = f'{datetime.utcnow().day}'
            temp_line += char
        silver_content += temp_line
print(silver_content)

with open("goldContent.txt", "r") as f:
    gold_content = ''
    for line in f:
        temp_line = ''
        for char in line:
            if char == "#":
                char = f"{gold_price}"
            elif char == "~":
                char = f'"{current_time}"'
            elif char == "*":
                char = f'{datetime.utcnow().minute}'
            elif char == "$":
                char = f'{datetime.utcnow().hour}'
            elif char == "@":
                char = f'{datetime.utcnow().second}'
            elif char == "&":
                char = f'{datetime.utcnow().day}'
            temp_line += char
        gold_content += temp_line
print(gold_content)

browser.get(lira_editor)
username_input = browser.find_element_by_id("user_login")
password_input = browser.find_element_by_id("user_pass")
login_button = browser.find_element_by_id("wp-submit")

username_input.send_keys(username)
print("Username entered")
password_input.send_keys(password)
print("Password entered")
login_button.click()
print("Logging In")

print("Waiting")
sleep(10)
print("Done waiting")

while True:
    try:
        open_editor()
        break
    except Exception:
        sleep(5)
        continue

change_script_tags(lira_content)
print("Lira tags Updated")
print("Update committed")

browser.get(gold_editor)

print("Waiting")
sleep(10)
print("Done waiting")

while True:
    try:
        open_editor()
        break
    except Exception:
        sleep(5)
        continue

change_script_tags(gold_content)
print("Gold tags Updated")
print("Update committed")

browser.get(silver_editor)

print("Waiting")
sleep(10)
print("Done waiting")

while True:
    try:
        open_editor()
        break
    except Exception:
        sleep(5)
        continue

change_script_tags(silver_content)
print("Silver tags Updated")
print("Update committed")


browser.quit()
print("Browser terminated")
