from configLoaderUtil import configLoaderUtil
import time
import os
from selenium import webdriver





def main():
    # print(configLoaderUtil.loadYaml('config.yml'))
    driver = webdriver.Chrome(os.path.expanduser('~/Desktop/chromedriver'))  # Optional argument, if not specified will search path.

    driver.get('http://www.google.com/')

    time.sleep(5) # Let the user actually see something!

    search_box = driver.find_element_by_name('q')

    search_box.send_keys('ChromeDriver')

    search_box.submit()

    time.sleep(5) # Let the user actually see something!

    driver.quit()
    

if __name__ == "__main__":
    main()