from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

## initiate browswer - change executable path as needed
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


## scrape mars websites - returns a dictionary of various data types
def scrape():
    
    browser = init_browser()
    
    ## Get latest news Title and Paragraph
    
    url ='https://mars.nasa.gov/news/'  #NASA
    
    browser.visit(url)
    time.sleep(2)  # allow time for browswer to redirect
    
    html = browser.html # collect html after redirect
    soup = BeautifulSoup(html, 'html.parser')
    
    # scrape first title
    titles = soup.find_all('div', class_='content_title')
    news_title = titles[0].text.strip()
    
    # scrape first paragraph
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraphs[0].text.strip()
    
    ## Get featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit'      #JPL
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    my_img_url = soup.find_all('div', class_='img')[0].find('img')['src']
    featured_image_url = 'https://www.jpl.nasa.gov/' + my_img_url
    
    ## Get Weather Data
    url = 'https://twitter.com/marswxreport?lang=en'    # Twitter
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    headlines = soup.find_all('div', class_='content')
    
    # had to make sure given tweet was tagged with Mar Weather
    # indexes first headline with 'Mars Weather', pulls description from that index
    count = 0   
    for headline in headlines:
        if headline.find('strong').text == 'Mars Weather':
            mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[count].text.strip()
            mars_weather = mars_weather.split("InSight ")[1].split('hPa')[0]   # cleaning unneccessary text
            break
        count += 1
        
    ## Mars Facts
    url = 'https://space-facts.com/mars/'   #Space-Facts.com
    tables = pd.read_html(url)
    myfacts_df = tables[0]
    myfacts_df['Metric'] = myfacts_df.iloc[:,0]
    myfacts_df['Value'] = myfacts_df.iloc[:,1]
    myfacts_df = myfacts_df.iloc[:,2:4]
    facts_table = myfacts_df.to_html()

    ## Hemispheres
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'   # Astrogeology.usgs.gov
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    my_hems_titles = soup.find_all('div', class_='description')
    
    titles = []  # appends all hemisphere titles
    img_urls = []  # appends all hemisphere img urls
    
    for item in my_hems_titles:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        
        my_title = item.find('h3').text   # takes title
        titles.append(my_title)
        
        browser.click_link_by_partial_text(my_title)   #goes to link using title to search
        html = browser.html            
        soup = BeautifulSoup(html, 'html.parser')
        
        
        big_img = soup.find_all('img', class_='wide-image')[0]['src']
        img_urls.append('https://astrogeology.usgs.gov' + big_img)   #takes img url of enhanced jpg :)
    
    # create dictionary for hemispheres
    hemispheres = [
    {"title": titles[0], "img_url": img_urls[0]},
    {"title": titles[1], "img_url": img_urls[1]},
    {"title": titles[2], "img_url": img_urls[2]},
    {"title": titles[3], "img_url": img_urls[3]},
]
    
    
    # dictionary to be returned
    my_data = {
        'news_title':news_title,
        'news_p':news_p,
        'facts_table': facts_table,
        'featured': featured_image_url,
        'mars_weather': mars_weather,
        'img_urls': hemispheres
    }
    
    print("Scraping complete")
    
    browser.quit()
    
    return my_data
    
    
    