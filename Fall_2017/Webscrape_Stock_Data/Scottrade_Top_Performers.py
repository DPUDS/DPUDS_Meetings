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
wiki = "https://research.scottrade.com/qnr/Public/InvestorTools/Performers?type=s&results_view=performing"

#Allowing for unverified handshake with website
context = ssl._create_unverified_context()

#Open up webpage
page = req.urlopen(wiki, context = context)

#Extract ALL html code from the webpage as a soup
soup = BeautifulSoup(page, "html.parser")

#Find the table within the soup for top performers
performers_table = soup.find('table', class_='sortable Performers mb15')

#Generate lists for all fields (see below for field descriptions)
A=[]
B=[]
C=[]
D=[]
E=[]
F=[]
G=[]
H=[]
I=[]

#Finds all row in the table (tr)
for row in performers_table.findAll("tr"):
    #Finds all cells in the table
    cells = row.findAll('td')
    if len(cells)==9: #Only extract table body not heading
        #Extract all data from the table into the lists
        A.append(cells[1].find(text=True))      # Symbol
        B.append(cells[2].find(text=True))      # Sector
        C.append(cells[3].find(text=True))      # Industry
        D.append(cells[4].find(text=True))      # Prior Close
        E.append(cells[5].find(text=True))      # 5 Day Change
        F.append(cells[6].find(text=True))      # 4 Week Change
        G.append(cells[7].find(text=True))      # 52 Week Change
        H.append(cells[8].find(text=True))      # Market Cap
        

#Create pandas dataframe of all lists
df=pd.DataFrame(A,columns=['Symbol'])
df['Sector']=B
df['Industry']=C
df['Prior_Close']=D
df['5_Day_Change']=E
df['4_Week_Change']=F
df['52_Week_Change']=G
df['Market_Cap']=H


#Show Scottrade's top performers
#print(df)