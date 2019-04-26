from django.shortcuts import render
import time
import requests
from bs4 import BeautifulSoup
import re
import pymssql
from selenium import webdriver
from urllib.parse import quote


def hello(request):
    PhoneList=OpenWeb()
    return render(request,'hello.html',{"phonelist":PhoneList})
def OpenWeb():
    driver=webdriver.Chrome()
    key='手机'
    url='https://search.jd.com/Search?keyword='+quote(key)+'&enc=utf-8'
    driver.get(url)
    driver.implicitly_wait(3)
    for i in range(10):
        driver.execute_script("var q=document.documentElement.scrollTop={0}".format(i*1000))
        time.sleep(1)
    phones_img_xpath=driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/img')
    imgs = [l.get_attribute('src') for l in phones_img_xpath]
    phones_price_xpath=driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i')
    price=[c.text for c in phones_price_xpath]
    phones_name_xpath=driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/em')
    name=[c.text for c in phones_name_xpath]
    phones=[]
    m=0
    n=1
    for i in imgs:
        phone={}
        phone['id']=n
        phone['img']=imgs[m]
        phone['name']=name[m]
        phone['price']=price[m]
        phones.append(phone)
        m=m+1
        if n==5:
            n=1
        else:
            n=n+1
    #SaveToSql(phones)
    #JDPhones=GetFromSql()
    return  phones


def SaveToSql(JDphones):
    conn = pymssql.connect(host='localhost', user='syy1', password='123', database='JDPhones', charset='utf8')
    cur = conn.cursor()
    try:
        for phones in JDphones:
            for phone in phones:
                cur.execute("insert into Movies values(%s,%s,%s,%s)",
                            (phone["img"], phone["name"], phone["price"]))
                conn.commit()
    except:
        print('false')
    cur.close()
    conn.close()


def GetFromSql():
    conn = pymssql.connect(host='localhost', user='syy1', password='123', database='JDPhones', charset='utf8')
    cur = conn.cursor()
    try:
        cur.execute("select * from Phone")
        ll = cur.fetchall()
        ml = []
        for i in ll:
            m = 0
            md = {}
            for j in i:
                if m == 1:
                    md["phoneimgs"] = j
                elif m == 2:
                    md["phonename"] = j
                elif m == 3:
                    md["phoneprice"] = j
                m = m + 1
            ml.append(md)
        return ml

    except:
        print('false')
    cur.close()
    conn.close()





