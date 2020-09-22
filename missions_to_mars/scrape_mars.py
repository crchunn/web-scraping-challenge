# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

from splinter import Browser
from bs4 import BeautifulSoup
import requests, contextlib, re, os
import pandas as pd
import time



def init_browser():
    executable_path = {"executable_path": "C:/Users/xtrad/Desktop/TheBoot/web-scraping-challenge/missions_to_mars/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)



def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    slide_elem = soup.select_one("ul.item_list li.slide")
    slide_title = slide_elem.find("div", class_='content_title').get_text()
    slide_body = slide_elem.find("div", class_='article_teaser_body').get_text()



    # browser = init_browser()
    # url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(url)



    #featured_image_url = browser.find_by_id("full_image")




    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    pictures = []
        
    featured_image_url = browser.find_by_css('a.product-item h3')
    for i in range(len(featured_image_url)):
    
        #print(featured_image_url)
        browser.find_by_css('a.product-item h3')[i].click()
        
        # Find and click the full image button

        # Find the more sample button and click that
        #browser.is_element_present_by_text('Sample', wait_time=1)
        more_info_elem = browser.links.find_by_text('Sample').first
        pictures.append(more_info_elem['href'])
        print(i)
        browser.back()
        
    print(pictures)



    # browser = init_browser()
    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.visit(url)

    # featured_image_url = browser.find_by_css('a.itemLink.product-item h3')
    # featured_image_url.click()



    # Find and click the full image button

    # Find the more sample button and click that
    # browser.is_element_present_by_text('Sample', wait_time=1)
    # more_info_elem = browser.links.find_by_partial_text('Sample')



    # img_url = more_info_elem.first['href']
    # img_url



    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)
        
    featured_image_url = browser.find_by_id("full_image")
    featured_image_url.click()
        
    # Find and click the full image button

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()
    # Parse the resulting html with soup
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    slide_fig = soup.select_one("figure.lede a img").get("src")


# bring in the tweets

    browser = init_browser()

    url = "https://twitter.com/MarsWxReport?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"
    browser.visit(url)
    time.sleep(5)

# make sure to use beautiful soup to parse the information
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    mars_weather = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
        mars_weather_tweet = mars_weather.find("p", "tweet-text").get_text()
        mars_weather_tweet
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather_tweet = soup.find('span', text=pattern).text
        mars_weather_tweet

        

# Just the facts

    facts_url = "https://space-facts.com/mars/"
    facts = pd.read_html(facts_url)
    facts

# parse down into the website to grab up some information

    facts_df = facts[0]
    facts_df.rename({0: 'Description', 1: 'Value'}, axis=1, inplace=True)
    facts_df


    facts_df = facts_df.to_html('marsfacts.html')
    
# once the info is pulled, slide into a dictionary


    mars_data = {
        'weather_tweet': mars_weather_tweet,
        'facts': facts_df,
        'img': slide_fig,
        'title': slide_title,
        'body': slide_body,
        'pictures': pictures

    }


# print all the data to insure it's arrival
    browser.quit()
    print(mars_data)



    return mars_data


