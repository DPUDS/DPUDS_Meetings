###################################################
#
# Scrape Scottrade's Top Performers
#
# Created by: Sam Showalter
# Creation Date: 2017-04-01
#
###################################################

import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request as req 
import ssl

#Link to scottrades list of top performing public companies
link = "https://research.scottrade.com/qnr/Public/InvestorTools/Performers?type=s&results_view=performing"

#Allowing for unverified handshake with website
context = ssl._create_unverified_context()

#Open up webpage
page = req.urlopen(link, context = context)

#Extract ALL html code from the webpage as a soup
soup = BeautifulSoup(page, "html.parser")

#Find the table within the soup for top performers
performers_table = soup.find('table', class_='sortable Performers mb15')


#Generate lists for all fields (see below for field descriptions)
symbol =[]
sector =[]
industry =[]
prior_close =[]
five_day_change =[]
four_week_change =[]
fifty2_week_change =[]
market_cap =[]


#Finds all row in the table (tr)
for row in performers_table.findAll("tr"):
    #Finds all cells in the table
    cells = row.findAll('td')
    if len(cells)==9: #Only extract table body not heading
        #Extract all data from the table into the lists
        symbol.append(cells[1].find(text=True))      # Symbol
        sector.append(cells[2].find(text=True))      # Sector
        industry.append(cells[3].find(text=True))      # Industry
        prior_close.append(cells[4].find(text=True))      # Prior Close
        five_day_change.append(cells[5].find(text=True))      # 5 Day Change
        four_week_change.append(cells[6].find(text=True))      # 4 Week Change
        fifty2_week_change.append(cells[7].find(text=True))      # 52 Week Change
        market_cap.append(cells[8].find(text=True))      # Market Cap
        

#Create pandas dataframe of all lists
df=pd.DataFrame(symbol,columns=['Symbol'])
df['Sector']=sector
df['Industry']=industry
df['Prior_Close']=prior_close
df['5_Day_Change']=five_day_change
df['4_Week_Change']=four_week_change
df['52_Week_Change']=fifty2_week_change
df['Market_Cap']=market_cap


#Show Scottrade's top performers
#print(df)