from django.shortcuts import render
import time
import requests
from bs4 import BeautifulSoup
import re
import pymssql
def getHTMLText(url,k):
    try:
        if (k==0):
            kw={}
        else:
            kw={'start':k,'filter':''}
        r=requests.get(url,params=kw,headers={'User-Agent':'Mozilla/4.0'})
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return False

def getData(html):
    soup=BeautifulSoup(html,"html.parser")
    movieList=soup.find('ol',attrs={'class':'grid_view'})
    ls=[]
    for movieli in movieList.find_all('li'):
        data={}
        movieHd=movieli.find('div',attrs={'class':'hd'})
        movieName=movieHd.find('span',attrs={'class':'title'}).getText()
        data['电影名']=movieName
        movieScore=movieli.find('span',attrs={'class':'rating_num'}).getText()
        data['电影评分']=movieScore
        movieEval=movieli.find('div',attrs={'class':'star'})
        movieEvalNum=re.findall(r'\d+',str(movieEval))[-1]
        data['电影评价人数']=movieEvalNum
        movieQuote=movieli.find('span',attrs={'class':'inq'})
        if(movieQuote):
            data['电影短评']=movieQuote.getText()
        else:
            data['电影短评']='无'
        ls.append(data)
    return ls
def hello(request):
    SaveToSql()
    MovieList=GetFromSql()
    return render(request,'hello.html',{"movielist":MovieList})

def SaveToSql():
    dburl='https://movie.douban.com/top250'
    k=0
    content=[]
    while k<=225:
        html=getHTMLText(dburl,k)
        time.sleep(2)
        k+=25
        content.append(getData(html))

    conn=pymssql.connect(host='localhost',user='syy1',password='123',database='DouBan',charset='utf8')
    cur=conn.cursor()
    try:
        for movie in content:
            for movie2 in movie:
                cur.execute("insert into Movies values(%s,%s,%s,%s)",(movie2["电影名"],movie2["电影评分"],movie2["电影评价人数"],movie2["电影短评"]))
                conn.commit()
    except:
        print('false')
    cur.close()
    conn.close()
def GetFromSql():
    conn=pymssql.connect(host='localhost',user='syy1',password='123',database='DouBan',charset='utf8')
    cur=conn.cursor()
    try:
        cur.execute("select * from Movies")
        ll=cur.fetchall()
        ml=[]
        for i in ll:
            m=0
            md={}
            for j in i:
                if m==1:
                    md["moviename"]=j
                elif m==2:
                    md["moviegrades"]=j
                elif m==3:
                    md["movieassess"]=j
                elif m==4:
                    md["movieshortassess"]=j
                m=m+1
            ml.append(md)
        return ml

    except:
        print('false')
    cur.close()
    conn.close()



