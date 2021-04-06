"""

Author = Parth Nipun Dave

This script is developed to fetch bollywood movie data from Wikipedia. It has used BS4 as scrapping tool.

Read readme.md for details.
"""











from bs4 import BeautifulSoup
import requests,urllib
import pandas as pd
import re
import time
import fetching_links as fl
import numpy as np
from tinydb import TinyDB,Query
db=TinyDB("movie_database.json")

month_list=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
discard_heading=["opening",'studio',"no.","production house","production company","language","music director","source","composer","studio (production house)","ref.","notescinematographer","references","external links","notes","see also","note","footnotes","sources", 'distributor', 'domestic collecion(india)', 'worldwide gross','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec',"january","february","march","april","may","june","july","august","september","october","november","december","ref","notes/music","sources / notes","music","studio (production house)","production house"]
movie_list=[]
not_content=["references","film companies","external links","notes","see also","note","footnotes","sources","#","2009 releases"]
grosser=["highest-grossing films","top-grossing productions","highest grossing films","highest-grossing","box office","top-grossing films","highest-grossing films (u.s.)","top-earning films","highest - grossing films","box office collection","top grossing films"]
movie_df=pd.DataFrame()
movie_list=[]
def beautify_text(value):
    chrs=re.findall("([a-z])([A-Z])",value)
    if "" not in chrs:

	    value=re.split("([a-z])([A-Z])",value)
	    print(value)
	    temp=value
	    for i in range(len(value)):
	        if value[i].islower():
	            value[i-1]=value[i-1]+value[i]
	        if value[i].isupper():
	            value[i+1]=value[i]+value[i+1]
	    for i in chrs:
	        for j in i:
	            value.remove(j)
	    print(",".join(value))
    return ",".join(value)

def movie_scrapper(links):
	global movie_df
	for url in links:
		
		print("AT -->",url)
		
		
		industry=url.split("_")[2]
		contents=[]
		soup_content=requests.get(url)
		soup_content=BeautifulSoup(soup_content.text,"html.parser")
		table=soup_content.select("table.wikitable")
		for content in soup_content.select("li.toclevel-1 span.toctext"):
			content=content.text.lower()
			if content in re.findall("^\d{1,4} in indian cinema|indian cinema in \d{1,4}$",content):
				pass
			else:
				if content not in not_content:
					if content in grosser:
						content="grosser"
					contents.append(content)
		if len(contents)>1:
			if "films" in contents:
				contents.remove("films")
			if len([i for i in contents if i in re.findall("^\d{1,4}",i)])>0:
				year="".join([i for i in contents if i in re.findall("^\d{1,4}",i)])
				if year=="1950":
					content="grosser"
					contents.append("grosser")
				contents.remove("".join([i for i in contents if i in re.findall("^\d{1,4}",i)]))
		print(contents)
		print("Len  Contents ",len(contents),"Len Table ",len(table))
		year=url.split("_")[-1]
		
		if len(table)>=len(contents) and "grosser" in contents and "dubbed films" not in contents:
			print("Sliced from begining 1st condition")
			if year in ["1979","1978","1981"]:
				table=table
			
			else:
				table=table[1:]
			if year =="2019":
				table=table[1:]
		if len(table)>len(contents) and "grosser" not in contents and "dubbed films" in contents and year=="1995":
			table=table[1:-1]
		if len(table)>len(contents)and "grosser"  in contents and "dubbed films"  in contents:
			table=table[1:-1]
		if len(table)==len(contents) and "grosser" not in contents and "dubbed films"  in contents:
			print("4th condition")
			table=table[:-1]
		if len(table)>len(contents) and "grosser" not in contents and "dubbed films"  in contents:
			print("3rd condition")
			table=table[:-1]
		if len(contents)==0 and len(table)>0:
			if year=="2005":
				table=table[1:]
			else:
				print("5th condition")
				table=table
		
			
		if len(contents)==len(table) and "grosser" in contents and "dubbed films" in contents:
			print("6th condition")
			if year in ["1991","1990","1982"]:
				table=table[:-1]
			else:
				table=table[1:-1]
		for tab in range(len(table)):
			headings=[]
			rough_head=[]
			values=[]
			tables=BeautifulSoup(str(table[tab]),"html.parser")
			for headers in tables.select("table.wikitable tr th"):
				headers=headers.text.lower()
				headers=headers.replace("\n","")

				if headers not in discard_heading:
					if headers=="cast and crew":
						headers='cast'
					if headers not in re.findall("^\d{1,2}",headers):
						headings.append(headers)
				if headers not in re.findall("^\d{1,2}",headers) and headers not in month_list:
					rough_head.append(headers)

			print("rough_head\n",rough_head)
			for data in tables.select("table.wikitable tr td"):
				year=url.split("_")[-1]
				value=data.text
				
				value=value.replace("\n","")
				if value=="":
					value="NA"
				if ''.join([x.lower() for x in re.sub("\ ","", value)  if x ]) not in month_list:
					

					if int(year)>=1991 and year not in ["2000","2002","2003","2004","2005","2006","2007"]:
						if data.a!=None and data.a.text in re.findall("^\d{1,2}|^ \d{1,2}",value):
								values.append(value)
						if value not in re.findall("^\d{1,2}|^ \d{1,2}",value):
							values.append(value)
					else:
						values.append(value)			
			start=0
			movie_dict={}
			if len(rough_head)!=0:
				if "opening" in rough_head and len(rough_head)<=5: 
					temp=headings
				elif "opening" in rough_head and len(rough_head)>5:
					print("here")
					temp=rough_head[1:]
				else:
					temp=rough_head
				for ind in range(0,len(values),len(temp)):
					if "title" in temp:
						title_ind=temp.index("title")
						movie_dict["title"]=values[title_ind]
					if "genre" in temp:
						genre_ind = temp.index("genre")
						movie_dict['genre']=values[genre_ind]
					if "cast" in temp:
						cast_ind=temp.index("cast")
						if int(year)>=2018:
							if values[cast_ind]=="NA":
								pass
							else:
								values[cast_ind]=beautify_text(values[cast_ind])
						movie_dict["cast"]=values[cast_ind]
					if "director" in temp:
						dir_ind=temp.index("director")
						if int(year)>=2018:
							if values[dir_ind]=="NA":
								pass
							else:
								values[dir_ind]=beautify_text(values[dir_ind])
						movie_dict["director"]=values[dir_ind]
					movie_dict["industry"]=industry
					movie_dict['year']=year
					db.insert(movie_dict)
					movie_list.append(movie_dict)
					movie_df=movie_df.append(movie_dict,ignore_index=True)
					print(movie_dict)
					for i in range(0,len(temp)):
						values.pop(0)
	return movie_list


if __name__=="__main__":
	links=fl.fetch_link_pages()
	movie_scrapper(links)
	movie_df=movie_df[["title","cast","director","genre","industry","year"]]
	print(movie_df)
	movie_df.to_csv("Movie_Dataset/BollywoodMovies_.csv",index=None)