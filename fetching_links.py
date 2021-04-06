from bs4 import BeautifulSoup
import requests,urllib
import pandas as pd
import re
import numpy as np
import files as f
lists=[]
# Fetch Link Pages
def fetch_link_pages():
    try:
        links = f.fetch_links()
        for url in links:
            response=requests.get(url)
            soup=BeautifulSoup(response.text,'html.parser')
            for i in soup.select("td.sidebar-content a"):
                link=i.attrs.get("href")
                if link==None:
                    link=url
                    if link.split("_")[-1] =="1890s":
                        pass
                    else:
                        if link not in lists:
                            lists.append(link)
                else:
                    if link not in lists:
                        if link.split("_")[-1] =="1890s":
                            pass
                        else:
                            lists.append("https://en.wikipedia.org"+link)
    except e:
        print(e)    
    return lists