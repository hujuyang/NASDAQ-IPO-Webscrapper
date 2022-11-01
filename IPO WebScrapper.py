# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 20:54:53 2022

@author: andyh
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date

driver = webdriver.Chrome(r"C:\Users\andyh\Documents\MyCoding\chromedriver")
driver.get("https://www.nasdaq.com/market-activity/ipos")
content = driver.page_source
soup = BeautifulSoup(content,features="lxml")


columns = []
tickers = []
exchanges = []
IPO_list = ""
class_table_with_title = "market-calendar-table market-calendar-table--with-title"
class_title = "market-calendar-table__title"
class_all_headers = "market-calendar-table__header"
class_header = "market-calendar-table__columnheader-text"
class_tablebody = "market-calendar-table__body"
class_row = "market-calendar-table__row" 
class_cell_content = "market-calendar-table__cell-content"

for table in soup.find_all('div',attrs={'class':class_table_with_title}):
    title = table.find('h3', attrs={'class':class_title}).text
    if title == 'Upcoming':
        headers = table.find('tr', attrs={'class':class_all_headers,'role':'row'})
        column_name  = headers.find_all('span', attrs={'class':class_header})
        for c in column_name:
            columns.append(c.text)
        
        rows = table.find_all('tr', attrs={'class':class_row})
        for row in rows:
            ticker = row.find('a',href=True)
            exchange = row.find('td', attrs={'data-column':"proposedExchange"})
            if ticker is not None:
                tickers.append(ticker.text)
            if exchange is not None:
                exchange = exchange.find('div',attrs={'class':class_cell_content})
                exchanges.append(exchange.text)

for i in range(len(tickers)):
    if 'NASDAQ' in exchanges[i]:
        IPO_list += 'NASDAQ' + ':' + tickers[i] + ','
    if 'NYSE' in exchanges[i]:
        IPO_list  += 'NYSE' + ':' + tickers[i] + ','        
            
        
with open(f'Upcoming IPO Tickers-{date.today().strftime("%B %d")}.txt','w') as t:
    t.write(IPO_list)
    


    
    