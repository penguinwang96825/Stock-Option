import os
import shutil
import requests
import time
import datetime
import warnings
import random
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
warnings.filterwarnings("ignore")


def get_file(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": 
                            r"C:\Users\YangWang\Desktop\Stock-Option\stock\\", 
                 "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    driver_path = r"./chromedriver.exe"
    driver = webdriver.Chrome(driver_path, options=options)

    url = "http://www.cboe.com/delayedquote/quote-table-download"
    driver.get(url)
    time.sleep(2 + random.random())

    soup = BeautifulSoup(driver.page_source, "html.parser")
    input_element = driver.find_element_by_xpath('//*[@id="txtTicker"]')
    input_element.send_keys(query)
    input_element.send_keys(Keys.ENTER)
    time.sleep(10 + random.random())
    driver.quit()
    
    Initial_path = "./stock/"
    filename = max([Initial_path + "\\" + f for f in os.listdir(Initial_path)], key=os.path.getctime)
    shutil.move(filename, os.path.join(Initial_path, r"{}.dat".format(query)))


def main():
	stock_path = "stock_config.txt"
	stock = open(stock_path, 'r').read().split('\n')
	for s in stock:
		get_file(query=s)
	print("Complete downloading!")

if __name__ == "__main__":
    main()