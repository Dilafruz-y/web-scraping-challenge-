#!/usr/bin/env python
# coding: utf-8



# Dependencies

import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup as bs 
from flask import Flask, render_template, redirect
import pymongo
from selenium import webdriver

 
def init_browser(): 

    #open chrome driver browser

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_dict ={}
   
    # Mars News
    # define url

    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)

    # create beautiful soup object 
    html = browser.html
    mars_news_s = bs(html, 'html.parser')



    # find the first news title
        
    news_title = mars_news_s.body.find("div", class_="content_title").text

    # find the paragraph associated with the first title

    news_p = mars_news_s.body.find("div", class_="article_teaser_body").text

    # close the browser


    print(f"The news title: \n{news_title}")
    print()
    print(f"The paragraph:  \n{news_p}")



    # JPL Mars Space Images - Featured Image
    # define url
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
            
    browser.visit(image_url)

    html = browser.html

    image_s = bs(html, 'html.parser')



    # Retrieve featured image link

    relative_image_path = image_s.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path
    print(f'The featured_image_url: \n{featured_image_url}')




    #Mars Facts

    # define url
    mars_facts_url = "https://space-facts.com/mars/"

    # read html into pandas
    mars_facts_table = pd.read_html(mars_facts_url)
    #mars_facts_tables
    # It returns 3 tables. The first has the data needed, so will convert to a dataframe and clean up nameing

    table_df1 = mars_facts_table[0]
    table_df1.columns = ["Description", "Value"]

    table_df1




    #convert to HTML
    mars_html_table = table_df1.to_html()
    print(mars_html_table)




    #Mars Hemispheres
    # define url
    usgs_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
                    
    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    hemispheres_soup = bs(hemispheres_html, 'html.parser')



    #Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
        
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
        
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
        hemisphere_image_urls.append(image_dict)

   



    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "fact_table": str(mars_html_table),
            "hemisphere_images": hemisphere_image_urls
        }
   
    browser.quit()
    return mars_dict







