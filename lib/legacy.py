# Старые неиспользуемые функции
def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def find_error(driver):
    canvas = driver.find_element_by_id("#canvas")
    filename = "./temp/" + random_word(10) + ".png"
    canvas.screenshot(filename)
    method = cv2.TM_SQDIFF_NORMED
    small_image = cv2.imread('error.png')
    large_image = cv2.imread(filename)
    result = cv2.matchTemplate(small_image, large_image, method)
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    MPx, MPy = mnLoc
    os.unlink(filename)
    # print(MPx, MPy)
    return 420 <= MPy <= 470


def approve_with_press_captcha(driver):
    print('Меняем окно')
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    try:
        print('Жмем на капчу, чтобы плагин начал ее решать')
        press_captcha(driver)
    except:
        traceback.print_exc()
    print('Ждем пока пройдется капча')
    sleep(20)
    # wait = WebDriverWait(driver, 10)
    # element = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/section/div[2]/div/div[6]/button')))
    try:
        element = driver.find_element_by_xpath('/html/body/div[1]/div/section/div[2]/div/div[6]/button')
        actions = ActionChains(driver)
        print('Закрываем окно капчи с картинками')
        actions.move_to_element_with_offset(element, -100, -30).click().perform()
        sleep(1)
        print('Жмем Approve')
        actions.move_to_element(element).perform()
        actions.click().perform()
    except:
        traceback.print_exc()


def press_captcha(driver):
    frames = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(frames[0])
    driver.find_element_by_class_name("recaptcha-checkbox-border").click()
    driver.switch_to.default_content()


# TODO:Поменять точки
def new_main(driver):
    try:
        if find_error(driver):
            sleep(random.uniform(150.0, 200.0))
            click(driver, 615, 318)
            click(driver, 615, 304)
        if (len(driver.window_handles) > 1):
            sleep(random.uniform(30.0, 40.0))
            if (len(driver.window_handles) > 1):
                handles = driver.window_handles
                shouldRefresh = False
                for handle in handles[1:]:
                    driver.switch_to_window(handle)
                    sleep(random.uniform(2.5, 3.0))
                    if "Loading Transaction" in driver.page_source:
                        driver.close()
                        shouldRefresh = True
                    else:
                        approve(driver)
                driver.switch_to_window(handles[0])
                if shouldRefresh == True:
                    sleep(random.uniform(10.5, 11.0))
                    driver.refresh()
                    sleep(random.uniform(20.5, 30.0))
                    click(driver, 403, 545)
                    sleep(random.uniform(15.5, 17.0))
                    click(driver, 660, 340)
                    sleep(random.uniform(10.5, 11.0))
        print("clicked")
        click(driver, 400, 615)
        sleep(random.uniform(0.010, 1.0))
        click(driver, 400, 475)
        sleep(random.uniform(0.010, 1.0))
        click(driver, 217, 577)
        sleep(3)
    except Exception as e:
        sleep(3)
