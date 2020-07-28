import requests
import time
import os
import datetime
import warnings
import random
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
warnings.filterwarnings("ignore")


def get_file(query):
    driver_path = r"./chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("download.default_directory={}".format(os.getcwd()))
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    url = "http://www.cboe.com/delayedquote/quote-table-download"
    driver.get(url)
    time.sleep(2 + random.random())

    soup = BeautifulSoup(driver.page_source, "html.parser")
    input_element = driver.find_element_by_xpath('//*[@id="txtTicker"]')
    input_element.send_keys(query)
    input_element.send_keys(Keys.ENTER)
    time.sleep(10 + random.random())
    driver.quit()

def read_this_month(path):
	file = open(path, 'r').read().split('\n')
	file = file[3: ]

	temp_list = []
	for element in file:
		temp_list.append(element.split(","))
	df = pd.DataFrame(temp_list)
	df = df.iloc[:, [0, 11, 10, 11, 21]]
	df.columns = ["Expiration Date", "Strike", "Call", "Strike", "Put"]

	this_month = int(pd.to_datetime('today').month)
	df_this_month = df.copy()

	df_this_month = df_this_month.dropna(axis=0)
	df_this_month["Date"] = df_this_month["Expiration Date"].apply(lambda x: pd.to_datetime(x))
	df_this_month["Date"] = df_this_month["Date"].apply(lambda x: str(x.date()))
	df_this_month['Date'] = df_this_month['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
	df_this_month['Month'] = df_this_month['Date'].apply(lambda x: datetime.datetime.strftime(x, '%m')).astype('int64')
	df_this_month = df_this_month[df_this_month["Month"] == this_month]
	df_this_month.set_index(df_this_month['Date'], drop=True, inplace=True)
	# Drop the date before today
	df_this_month = df_this_month.loc[pd.to_datetime('today').date():]
	df_this_month.reset_index(drop=True, inplace=True)
	df_this_month["Call"] = df_this_month["Call"].apply(lambda x: int(x))
	df_this_month["Put"] = df_this_month["Put"].apply(lambda x: int(x))
	df_call_1 = df_this_month.groupby(df_this_month.iloc[:, 1])["Call"].agg(sum).sort_values(ascending=False)
	df_call_1 = pd.DataFrame(df_call_1)
	df_call_1.reset_index(drop=False, inplace=True)
	df_put_1 = df_this_month.groupby(df_this_month.iloc[:, 1])["Put"].agg(sum).sort_values(ascending=False)
	df_put_1 = pd.DataFrame(df_put_1)
	df_put_1.reset_index(drop=False, inplace=True)
	df_1 = pd.concat([df_call_1, df_put_1], axis=1)
    
	return df_1

def read_next_month(path):
	file = open(path, 'r').read().split('\n')
	file = file[3: ]

	temp_list = []
	for element in file:
		temp_list.append(element.split(","))
	df = pd.DataFrame(temp_list)
	df = df.iloc[:, [0, 11, 10, 11, 21]]
	df.columns = ["Expiration Date", "Strike", "Call", "Strike", "Put"]

	next_month = int(pd.to_datetime('today').month) + 1
	df_next_month = df.copy()

	df_next_month = df_next_month.dropna(axis=0)
	df_next_month["Date"] = df_next_month["Expiration Date"].apply(lambda x: pd.to_datetime(x))
	df_next_month["Date"] = df_next_month["Date"].apply(lambda x: str(x.date()))
	df_next_month['Date'] = df_next_month['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
	df_next_month['Month'] = df_next_month['Date'].apply(lambda x: datetime.datetime.strftime(x, '%m')).astype('int64')
	df_next_month = df_next_month[df_next_month["Month"] == next_month]
	df_next_month.set_index(df_next_month['Date'], drop=True, inplace=True)
	# Drop the date before today
	df_next_month = df_next_month.loc[pd.to_datetime('today').date():]
	df_next_month.reset_index(drop=True, inplace=True)   
	df_next_month["Call"] = df_next_month["Call"].apply(lambda x: int(x))
	df_next_month["Put"] = df_next_month["Put"].apply(lambda x: int(x))
	df_call_2 = df_next_month.groupby(df_next_month.iloc[:, 1])["Call"].agg(sum).sort_values(ascending=False)
	df_call_2 = pd.DataFrame(df_call_2)
	df_call_2.reset_index(drop=False, inplace=True)
	df_put_2 = df_next_month.groupby(df_next_month.iloc[:, 1])["Put"].agg(sum).sort_values(ascending=False)
	df_put_2 = pd.DataFrame(df_put_2)
	df_put_2.reset_index(drop=False, inplace=True)
	df_2 = pd.concat([df_call_2, df_put_2], axis=1)

	return df_2

def certain_date_option(path, input_date):
	path = path.lstrip().rstrip()
	file = open(path, 'r').read().split('\n')
	file = file[3: ]

	temp_list = []
	for element in file:
	    temp_list.append(element.split(","))
	df = pd.DataFrame(temp_list)
	df = df.iloc[:, [0, 11, 10, 11, 21]]
	df.columns = ["Expiration Date", "Strike", "Call", "Strike", "Put"]

	this_month = int(pd.to_datetime('today').month)
	df_temp = df.copy()

	df_temp = df_temp.dropna(axis=0)
	df_temp["Date"] = df_temp["Expiration Date"].apply(lambda x: pd.to_datetime(x))
	df_temp["Date"] = df_temp["Date"].apply(lambda x: str(x.date()))
	df_temp['Date'] = df_temp['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
	df_temp['Month'] = df_temp['Date'].apply(lambda x: datetime.datetime.strftime(x, '%m')).astype('int64')
	df_temp = df_temp[df_temp["Month"] == this_month]
	df_temp.set_index(df_temp['Date'], drop=True, inplace=True)
	# Drop the date before today
	df_temp = df_temp.loc[pd.to_datetime('today').date():]
	df_temp = df_temp[df_temp["Date"] == pd.to_datetime(input_date)]
	df_temp.reset_index(drop=True, inplace=True)
	df_temp["Call"] = df_temp["Call"].apply(lambda x: int(x))
	df_temp["Put"] = df_temp["Put"].apply(lambda x: int(x))
	df_call = df_temp.groupby(df_temp.iloc[:, 1])["Call"].agg(sum).sort_values(ascending=False)
	df_call = pd.DataFrame(df_call)
	df_call.reset_index(drop=False, inplace=True)
	df_put = df_temp.groupby(df_temp.iloc[:, 1])["Put"].agg(sum).sort_values(ascending=False)
	df_put = pd.DataFrame(df_put)
	df_put.reset_index(drop=False, inplace=True)
	df_final = pd.concat([df_call, df_put], axis=1)

	return df_final

def main():
	this_month = int(pd.to_datetime('today').month);
	next_month = this_month + 1
	today = str(pd.to_datetime('today').date())

	query = input("Stock name: ")
	question = input("Do you need to re-download stock data? (yes/no)\n")
	if question.lower() == "yes":
		get_file(query=query)
		time.sleep(1)
	file = input("File path: ")
	input_month = input("Which month do you need?\nThis month press 1.\nNext month press 2.\n")
	if input_month == str(1):
		df_this_month = read_this_month(file)
		input_date = input("Whole month or single date?\nWhole month press 1.\nSingle date press 2.\n")
		if input_date == str(1):
			print(df_this_month)
			df_this_month.to_csv("./data/{}_m{}_{}.csv".format(query, this_month, today), index=False)
		if input_date == str(2):
			certain_input_date = input("Type in certain date: (Format: 2020-07-28)\n")
			df_3 = certain_date_option(file, certain_input_date)
			print(df_3)
			df_3.to_csv("./data/{}_single_{}.csv".format(query, certain_input_date), index=False)
	if input_month == str(2):
		df_next_month = read_next_month(file)
		print(df_next_month)
		df_next_month.to_csv("./data/{}_m{}_{}.csv".format(query, next_month, today), index=False)

	print("CSV files are in current directory!")

if __name__ == "__main__":
	main()