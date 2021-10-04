from time import sleep

import inflect
from selenium import webdriver

# api_key = 'acc_dc24b556085e601'
# api_secret = '7b61bb6a01a70853a6b1e4e9a1016f83'
# image_path = 'D://Users//headneZzz//Desktop//BotsAlien//temp//1234556124.png'
#
# response = requests.post(
#     'https://api.imagga.com/v2/tags?language=ru',
#     auth=(api_key, api_secret),
#     files={'image': open(image_path, 'rb')})
#
# dict = response.json()
# print(dict['result']['tags'])
from selenium.webdriver import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('mute-audio')
chrome_options.add_argument("window-size=800,600")
driver = webdriver.Chrome(
    executable_path='D://Users//headneZzz//Desktop//BotsAlien//chromedriver.exe',
    options=chrome_options
)

try:
    driver.get('https://www.google.com/recaptcha/api2/demo')
except:
    pass

sleep(5)
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
driver.find_element_by_class_name("recaptcha-checkbox-border").click()
elements = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(elements[0])
driver.switch_to.default_content()

# wait img frame then switch
sleep(3)
iframe = driver.find_elements_by_tag_name("iframe")
print(len(iframe))
driver.switch_to.frame(iframe[2])
p = inflect.engine()  # init inflect
verify_button = driver.find_elements_by_id("recaptcha-verify-button")
print(driver.find_elements_by_tag_name("strong")[0].text)
driver.switch_to.default_content()
element = driver.find_elements_by_id("recaptcha-demo-submit")[0]
actions = ActionChains(driver)
actions.move_to_element(element).perform()
actions.click().perform()


# testo = p.singular_noun(driver.text)  # plural word to singular
# print(testo)
sleep(3600)
