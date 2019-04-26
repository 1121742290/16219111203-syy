import requests
from bs4 import BeautifulSoup
import re
import time
import sys

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
        movieHd=movie.find('div',attrs={'class':'hd'})
        movieName=movieHd.find('span',attrs={'class':'title'}).getText()
        data['电影名']=movieName
        movieScore=movieli.find('span',attrs={'class':'rating_num'}).getText()
        data['电影评分']=movieScore
        movieEval=movieli.find('div',attrs={'class':'star'})
        movieEvalNum=re.findall(r'\d+',str(movieEval))[-1]
        data['电影评价人数']=movieEvalNum
        movieQuote=movieli.find('span',attrs={'class':'inq'})
        if(movieQuote):
            data['电影短评']=movieQuote
        else:
            data['电影短评']='无'
        ls.append(data)
    return ls
        


 