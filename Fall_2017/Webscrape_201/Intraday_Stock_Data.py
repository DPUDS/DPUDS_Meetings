###################################################
#
# Intraday Minute-to-Minute Stock Data Webscrape
#
# Created by: Sam Showalter
# Creation Date: 2017-08-01
#
###################################################


###########################################
#
# Import Dependencies and Data Collection
#
###########################################

from bs4 import BeautifulSoup
import urllib.request as req 
import ssl
import pandas as pd
import datetime as dt
import time
import numpy as np
import os

###########################################
#
#          Set Meta-parameters
#
###########################################

#URl dictionary of sites that could be web-scraped
URL_dict = {'yahoo': 'https://finance.yahoo.com/quote/STOCK?p=STOCK',
			'NASDAQ': 'http://www.nasdaq.com/symbol/STOCK',
			'bloomberg': 'https://www.bloomberg.com/quote/STOCK:US',
			'reuters': 'http://www.reuters.com/finance/stocks/overview?symbol=STOCK.O'}

#Set ssl context to allow for an unverified handshake with a network site
ssl_context = ssl._create_unverified_context()


###########################################
#
#          Function Development
#
###########################################

'''
This is the yahoo ohlcv (open, high, low, close, volume)
webscraping engine. This function will return the most 
recent stock price and volume as found on the yahoo
finance webpage.

# ticker = any stock ticker, lower or uppercase
'''
def bloomberg_minute_ohlcv_data(ticker):

	#Creates the link needed to contact yahoo finance
	link  = URL_dict['bloomberg'].replace('STOCK',ticker.lower())

	#Returns stock price and volume as float values
	try:

		#Opens the URL link created above
		page = req.urlopen(link, context = ssl_context)

		#Extracts all html data from the page opened above
		soup = BeautifulSoup(page, "html.parser")

		if soup is not None:

			#Digging through html to find correct tags (classes) for stock price
			price = soup.find('span', class_ = "priceText__1853e8a5").find(text = True)
			price = price.replace(',','')

			#Refining down html tags for volume [(6th) row of the vol_table, within vol_class]
			volume = soup.find('section',class_= "dataBox volume numeric").find('div',class_ = "value__b93f12ea").find(text = True)
			volume = volume.replace(',','')


		#If price or volume comes back as a NoneType
		if price is not None and volume is not None:
			#Returns stock data and price as float values
			price, volume = float(price), float(volume)

			return price, volume

		#If soup object returns as NoneType
		else:
			print("\nError in scraping data, soup object returned as NoneType")

			time.sleep(1)
			print("Re-scraping\n")
			bloomberg_minute_ohlcv_data(ticker)
			


	# If stock data ill-formatted, scraping attempt is skipped
	# Sometimes data is reported as N/A briefly as it changes
	except Exception as e:
			print("\nError in scraping data, current scrape attempt skipped")
			print("Message: %s"%(e))

			time.sleep(1)
			print("Re-scraping\n")
			bloomberg_minute_ohlcv_data(ticker)
			


'''
Function helper to prevent things from erroring out
'''
def engine_try(engine):
	try:
		if eval(engine) is not None:
			#Gets price and volume data
			price, volume = eval(engine)

			return price, volume

	except Exception as e:
		print("\nError in evaluating scraping engine")
		print("Message: %s"%e)

		time.sleep(1)
		print("Re-scraping.\n")
		engine_try(engine)


'''
This is the master function for webscraping intraday stock
data on a minute to minute basis. Waiting until the top of 
the next minute, the get_ohlcv_data function notifies the 
user the time that the scrape starts. It then pulls stock 
price and volume data a total of five times over the course
of a given minute. The open, high, low, close, and average
volume are then calculated from this. Every minute, a new
row is added with ohlcv features, as well as a timestamp.
Once the duration (in minutes) is over, all of the collected 
data is saved as a csv file, named in the format:

[*stock_ticker*]_minute_ohlcv_data_[*date*].csv

# ticker - Any stock ticker
# provider - any website provider in URL_dict
  *NOTE* ONLY THE YAHOO SCRAPING ENGINE HAS BEEN CREATED
# duration - number of minutes for which the user wants data
'''
def get_ohlcv_data(ticker, provider, duration):

	#Stores list of all scraped data, one row per minute.
	#This is what is stored as a csv eventually.
	master_stock_data_list = []

	#Creates a string with the necessary code to execute the given engine.given
	#(e.g. 'yahoo_minute_ohlcv_data('GOOG')')
	engine = str(provider) + '_minute_ohlcv_data(\'' + ticker + '\')'

	#Intializing count variables for duration and scrape counts
	scrape_count = 0
	actual_duration = 0

	#Initializing price and volume lists for intra-minute scrapes
	price_list = []
	vol_list = []

	#Will turn to true at the top of the next minute. Allows Web-scrape pulls
	# to be organized.
	scrape_start = False

	#Initializes all datetime values for starting the scrape
	now = dt.datetime.now()
	#Rounds down current time to the most recent minute
	now = dt.datetime.strptime(now.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	#Adds a minute to the rounded down time
	start = now + dt.timedelta(minutes = 1, seconds = -now.second)

	#Pre-execution of web-scraping engine
	while not scrape_start:

		#If the time has reached the next minute, begin execute sequence by changing scrape_start
		if dt.datetime.now() >= start:
			scrape_start = True
			next_scrape = dt.datetime.strptime(dt.datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
			print('\nScrape started at %s and will run for %s minute(s) until %s\n'%(str(dt.datetime.now())[11:-7], 
																					 duration, 
																					 (dt.datetime.now() + dt.timedelta(minutes = duration)).strftime('%Y-%m-%d %H:%M')))

		#Notify the user that the scraping engine is still waiting.
		else:
			print('Scrape starting in %s seconds'%str((start - dt.datetime.now()))[5:-7])

			#Pauses the sequence for 1 second
			time.sleep(1)

	#Main execution loop
	while scrape_start and actual_duration < duration:

		#Resets after the scraper has pulled 5 times in one minute
		while scrape_count < 5:

			if dt.datetime.now() >= next_scrape:

				price, volume = engine_try(engine)

				#Add price and volume data to respective lists
				price_list.append(price)
				vol_list.append(volume)

				#Amend next_scrape time to be ten seconds later (allows pause)
				next_scrape += dt.timedelta(seconds = 10)

				#Increase scrape count by one
				scrape_count += 1

		#Gather all necessary data after scraping five times. (Date + ohlcv)
		Date_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
		min_open = price_list[0]
		min_high = max(price_list)
		min_low = min(price_list)
		min_close = price_list[len(price_list) - 1]
		min_avg_volume = int(np.mean(vol_list))

		#Create a row with all necessary data
		row = [Date_time, min_open, min_high, min_low, min_close, min_avg_volume]

		#Add row to master data list
		master_stock_data_list.append(row)

		#Notify user of the added row
		print("[%s] Row Stored"%Date_time)

		#Reset time parameters, counts, and temporary lists
		scrape_count = 0
		next_scrape += dt.timedelta(seconds = 10)
		price_list = []
		vol_list = []
		actual_duration += 1

	#Notify user when the webscrape has finished
	print("\n[%s] Scrape Finished.\n"%(dt.datetime.now().strftime('%Y-%m-%d %H:%M')))

	#Create a DataFrame of all the gathered stock data, and remove dummy index
	stock_df = pd.DataFrame(master_stock_data_list, columns = ['DateTime', 'Open', 'High', 'Low', 'Close', "Avg_Volume"])
	stock_df.set_index('DateTime', inplace = True)

	#print(stock_df)

	#Parameters to create file name
	date = dt.datetime.now().strftime('%Y-%m-%d')
	file_name = ticker.upper() + '_Intraday_Stock_Data_' + date + '.csv'

	#Store stock data scrapings as a csv file
	stock_df.to_csv(file_name, sep = ',')
	print('File saved at location: %s'%(os.getcwd()))



'''
Main method. All variables are defined as they were for get_ohlcv_data.
Only new addition is changing the working directory.
'''
def main(ticker, provider, duration):

	#Change this to your current working directory of choice
	os.chdir('/Users/Sam/Documents/Python/DPUDS/DPUDS_Meetings/Fall_2017/Webscrape_201')

	get_ohlcv_data(ticker, provider, duration)

main('AMZN','bloomberg', 3)
