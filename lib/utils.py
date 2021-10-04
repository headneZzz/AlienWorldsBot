import random
import threading
import traceback
import zipfile
from telnetlib import EC
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from lib.proxy import manifest_json, create_background_js


def click(driver, x, y):
    action_chains = ActionChains(driver)
    element = driver.find_element_by_id("#canvas")
    action_chains.move_to_element_with_offset(element, x, y).click().perform()


def get_simple_driver(url, user_data_dir, profile_directory, executable_path):
    chrome_options = Options()
    chrome_options.add_argument('mute-audio')
    chrome_options.add_argument('user-data-dir=' + user_data_dir)
    chrome_options.add_argument('--profile-directory=' + profile_directory)
    chrome_options.add_argument("window-size=800,600")
    driver = webdriver.Chrome(
        executable_path=executable_path,
        options=chrome_options
    )

    try:
        driver.get(url)
    except:
        pass

    return driver


def get_proxy_driver(url, proxy, user_data_dir, profile_directory, executable_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('mute-audio')
    chrome_options.add_argument('user-data-dir=' + user_data_dir)
    chrome_options.add_argument('--profile-directory=' + profile_directory)
    chrome_options.add_argument("window-size=800,600")
    proxy_plugin_file = 'proxy_auth_plugin.zip'
    proxy = proxy.replace('@', ':')
    proxy_config = proxy.split(':')
    # captcha_plugin = 'anticaptcha-plugin_v0.52.zip'
    # chrome_options.add_extension(captcha_plugin)

    with zipfile.ZipFile(proxy_plugin_file, 'w') as zp:
        zp.writestr('manifest.json', manifest_json)
        zp.writestr('background.js', create_background_js(*proxy_config))
    chrome_options.add_extension(proxy_plugin_file)
    driver = webdriver.Chrome(
        executable_path=executable_path,
        chrome_options=chrome_options)
    driver.minimize_window()
    try:
        driver.get(url)
    except:
        pass

    return driver


def close_approve_window(driver):
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    driver.close()
    return_to_game(driver)


def buttons_pressing(driver):
    print('Жмем закрыть ошибку')
    click(driver, 570, 120)
    sleep(random.uniform(1, 2))
    print('Жмем закрыть предмет')
    click(driver, 650, 55)
    sleep(random.uniform(1, 2))
    print('Жмем Mine')
    click(driver, 390, 410)
    sleep(random.uniform(1, 2))
    print('Жмем Claim')
    click(driver, 320, 290)
    sleep(random.uniform(1, 2))
    print('Жмем Mining Hub')
    click(driver, 210, 375)
    sleep(random.uniform(1, 2))


def mining(driver, user):
    t = threading.currentThread()
    approve_windows_count = 1
    approve_try_count = 1
    while getattr(t, "do_run", True):
        try:
            if len(driver.window_handles) > 1:
                if approve_try_count > 7:
                    approve_try_count = 1
                    approve_windows_count += 1
                    print('Слишком много попыток, закрываем страницу подтверждения')
                    close_approve_window(driver)
                    login(driver, user)
                else:
                    print('Обработка подтверждения')
                    print('Попыток: ' + str(approve_try_count))
                    sleep(2)
                    try:
                        approve(driver, user)
                    except:
                        pass
                    approve_try_count += 1
            else:
                approve_try_count = 1
                print('Майнинг')
                buttons_pressing(driver)
                sleep(3)
        except:
            traceback.print_exc()
            sleep(3)


def get_auth_code(driver):
    driver.execute_script('''window.open("https://e.mail.ru/inbox/?back=1&afterReload=1","_blank");''')
    sleep(10)
    driver.find_element_by_xpath(
        '/html/body/div[5]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div[1]/div/div/div[1]/div/div/div/a[1]').click()
    sleep(10)
    auth_code = driver.find_element_by_xpath(
        '/html/body/div[5]/div/div[1]/div[1]/div/div[2]/span/div[2]/div/div/div/div/div/div/div[2]/div[1]/div[3]'
        '/div[2]/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/table/tbody/tr[3]/td/p[2]').text()
    print(auth_code)
    driver.close()
    return auth_code


def return_to_game(driver):
    driver.switch_to.window(driver.window_handles[0])
    driver.minimize_window()


def approve_login(driver, user):
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[3]/button').click()
    sleep(5)
    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input').send_keys(user['mail'])
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input').send_keys(user['pass'])
    sleep(40)
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]').click()
    sleep(10)
    if len(driver.current_url == 'https://wallet.wax.io/dashboard'):
        driver.close()
    else:
        # TODO: вставка кода и закрытие страницы
        print(get_auth_code(driver))


def approve(driver, user):
    print('Меняем окно')
    driver.switch_to.window(driver.window_handles[1])
    try:
        approve_login(driver, user)
    except NoSuchElementException:
        try:
            sleep(2)
            i = 0
            elem = driver.find_element_by_xpath('//*[@id="root"]/div/section/div[2]/div/div[5]/button')
            while i < 125:
                sleep(0.5)
                prop = elem.get_property('disabled')
                if not prop:
                    break
                i += 1
            elem.click()
            print('Жмем Approve')
        except:
            traceback.print_exc()
    except:
        traceback.print_exc()
    finally:
        return_to_game(driver)


def login(driver, user):
    print('Перезагрузили браузер')
    driver.refresh()
    print('Ждем 30 сек')
    sleep(30)
    print('Нажали на логин')
    click(driver, 390, 345)
    print('Ждем 30 сек')
    sleep(30)
    if len(driver.window_handles) > 1:
        login_user(driver, user)
    print('Нажали на логин майн')
    click(driver, 645, 150)


def click_button(button):
    not_clicked = True
    while not_clicked:
        try:
            button.click()
            not_clicked = False
        except:
            pass


def login_user(driver, user):
    driver.switch_to.window(driver.window_handles[1])
    # driver.execute_script('window.sessionStorage.clear()')
    # driver.refresh()
    try:
        sleep(15)
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[1]/input') \
            .send_keys(user['mail'])
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[5]/div/div/div/div[1]/div[2]/input') \
            .send_keys(user['pass'])
    except:
        traceback.print_exc()

    i = 0
    elem = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/div[5]/div/div/div/div[5]/button[1]')
    while i < 125:
        sleep(0.5)
        prop = elem.get_property('disabled')
        if not prop:
            break
        i += 1
    elem.click()
    print('Жмем Login')
    # TODO ввод кода с почты
    sleep(15)
    return_to_game(driver)


def stack_wax(driver):
    driver.get('https://wallet.wax.io/dashboard')
    driver.find_element_by_xpath('/html/body/div/div/div[1]/div/div[3]/img').click()
    driver.find_element_by_xpath('/html/body/div/div/div[4]/div[2]/button[3]').click()
    cpu_load = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/div[5]/div[1]/div[1]/svg/text[1]').text()
    cpu_load = int(cpu_load.replace('%', ''))
    if cpu_load >= 90:
        driver.find_element_by_name('amount').send_keys('1').submit()


def main(driver, user):
    while True:
        login_thread = threading.Thread(target=login, args=[driver, user])
        print('Старт логина')
        login_thread.start()
        login_thread.join()
        main_thread = threading.Thread(target=mining, args=[driver, user])
        print('Старт майнинг')
        main_thread.start()
        sleep(3600)
        print('Стоп майнтнг')
        main_thread.do_run = False
        main_thread.join()
        sleep(random.uniform(600.5, 900.0))
