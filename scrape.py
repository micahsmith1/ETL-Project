# Dependencies 
import os
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pandas as pd
from flask import Flask, redirect, render_template, jsonify
import time
from selenium import webdriver
import lxml
import urllib
from sqlalchemy import create_engine
import sqlalchemy

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection 
db = client.quotes
collection = db.quotes

# ENTIRE Quote List 
total_quotes=[]
# Counter
__id = 0 

for r in range(1,11):
    url=f'http://quotes.toscrape.com/page/{r}'
    response=requests.get(url)
    soup=bs(response.text, "lxml")

    ascrape=soup.find_all('div',{'class':'quote'})
    for a in ascrape:
        # ID Number 
        __id += 1 
        
        # Scrape Quote 
        quote=a.find('span', class_='text').text
        
        # Scrape Author Name 
        author_name=a.find('small', class_='author').text
        # Scrape Tags 
        tags_list=[]
        tags=a.find('div', class_='tags').find_all('a')
        for tag in tags:
            tag_text=tag.text.strip()
            tags_list.append(tag_text)
            
        # New URL for author details 
        href = a.a["href"]
        author_url = f'http://quotes.toscrape.com{href}'
        author_response = requests.get(author_url)
        author_soup = bs(author_response.text, 'lxml')
        
        # Scrape Author Details (Birthdate and Description)
        author_born = author_soup.find('span', class_ = 'author-born-date').text
        author_desrp = author_soup.find('div', class_ = 'author-description').text
        
        # Author Details Dictionary 
        author = {
            "name": author_name,
            "birthdate": author_born,
            "description": author_desrp
        }
        
        # ENTIRE Quote Dictionary to be inserted into MongoDB
        data = {
            '__id': __id,
            'quote': quote,
            'author': author,
            'tags': tags_list,
        }
        total_quotes.append(data)
        
        # Insert dictionary into MongoDB as a document 
        collection.insert_one(data)

# store csv into df
csv_file = "resources/quotes.csv"
quotes_df = pd.read_csv(csv_file)
quotes_df.head()

# review columns
quotes_df.columns

# clean df
quotes_df.columns = ['quote_id', 'id', 'text', 'name', 'born',
       'description', 'tags']

# select columns for new quotes df
new_quotes_df = quotes_df[['id', 'name', 'text']].copy()


# select columns for new author info df
new_author_df = quotes_df[['id', 'name', 'born', 'description']].copy()


# select columns for new tags df
new_tag_df = quotes_df[['id', 'quote_id', 'tags']].copy()

# connect to postgresql
rds_connection_string = "postgres://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o"
engine = create_engine(f'postgresql://lptdkrurwitgwv:3c931e0ab2fd366ac76902898dacfe8e0eeeabc5b2b222b12a48cefbc52c3fa5@ec2-34-237-236-32.compute-1.amazonaws.com:5432/d7e1q92pf06r6o')

# load quotes df into postgresql
new_quotes_df.to_sql(name='quotes', con=engine, if_exists='append', index=False)

# load author df into postgresql
new_author_df.to_sql(name='author', con=engine, if_exists='append', index=False)

# load tags df into postgresql
new_tag_df.to_sql(name='tags', con=engine, if_exists='append', index=False)