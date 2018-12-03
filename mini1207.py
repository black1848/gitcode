import math
import time
import csv
import calendar
import codecs
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
from urllib.request import urlopen
import os

def insert_data(cos):
    conn = pymysql.connect(host="localhost", user="root", password="root",
                        db='mycrawling', charset="utf8")
    cur = conn.cursor()
    sql = """ INSERT INTO cosdac(code,name,npr,op,creper,msh,mbh,tr_ct,tr_pr,tpr,hpr,lpr,acpr,money,tcoun,totpr,what,date)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql, cos)
    conn.commit()
    conn.close()

main_url = "http://marketdata.krx.co.kr/mdi#document=040602"
driver = webdriver.Chrome("C:/driver_craw/chromedriver.exe")
driver.get(main_url)
time.sleep(3)
driver.find_element_by_css_selector("#market_gubun2a87ff679a2f3e71d9181a67b7542122c").click()
time.sleep(1)
year = 2018
month = 11
day = 30
ct = 15
wday = 5

li = []

while ct <= 18:
    f = open("holiday%s.csv" % ct, 'r')
    rdr = csv.reader(f)
    for line in rdr:
        li.append(line)
    ct += 1
    f.close()

while year >= 2017:
    day -= 1
    wday -= 1
    if day == 0:
        month -= 1
        if month == 0:
            year -=1
            if year == 14:
                break
            month = 12
        day = calendar.monthrange(year, month)[1]
    if wday == 0:
        wday = 7
        continue
    if wday == 6:
        continue
    
    if month < 10 and day < 10:
        date = str(year) + "0" + str(month) + "0" + str(day)
    elif day < 10:
        date = str(year) + str(month) + "0" + str(day)
    elif month < 10:
        date = str(year) + "0" + str(month) + str(day)
    else:
        date = str(year) + str(month) + str(day)

    if [date] in li:
        continue

    elem = driver.find_element_by_id("schdated3d9446802a44259755d38e6d163e820")
    elem.clear()
    elem.send_keys(date)
    driver.find_element_by_css_selector("#btnidc81e728d9d4c2f636f067f89cc14862c").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='6512bd43d9caa6e02c990b0a82652dca']/button[3]").click()
    time.sleep(2)
    li1 = []
    f = codecs.open("C:/Users/Playdata/Downloads/data.csv", 'r', 'utf-8')
    rdr = csv.reader(f)
    print(rdr)
    for line in rdr:
        if line[1] == "종목명":
            continue
        line.append(date)
        li1.append(line)
    f.close()
    os.remove("C:/Users/Playdata/Downloads/data.csv")
    for cos in li1:
        insert_data(cos)

