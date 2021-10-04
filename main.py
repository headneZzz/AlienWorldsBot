from lib.utils import *

user = {
    'mail': '',
    'pass': '',
}

url = 'https://play.alienworlds.io/'
user_data_dir = 'D://Users//headneZzz//Desktop//BotsAlien//main'
profile_directory = 'Profile 15'
executable_path = 'D://Users//headneZzz//Desktop//BotsAlien//chromedriver.exe'
driver = get_simple_driver(url, user_data_dir, profile_directory, executable_path)
input("Press Enter to continue")

main(driver, user)
