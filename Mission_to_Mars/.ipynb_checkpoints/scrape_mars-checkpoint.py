from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    
    browser = init_browser()
    
    
    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    titles = soup.find_all('div', class_='content_title')
    news_title = titles[0].text.strip()
    
    paragraphs = soup.find_all('div', class_='article_teaser_body')
    news_p = paragraphs[0].text.strip()
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=mars&category=featured#submit'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA16029_ip.jpg'
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text.strip()
    mars_weather = mars_weather.split('InSight ')[1].split('hPap')[0]
    
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    myfacts_df = tables[0]
    myfacts_df['Metric'] = myfacts_df.iloc[:,0]
    myfacts_df['Value'] = myfacts_df.iloc[:,1]
    myfacts_df = myfacts_df.iloc[:,2:4]
    myfacts_str = myfacts_df.to_html()
    myfacts_str = myfacts_str.replace('\n', '')
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    my_hems_titles = soup.find_all('div', class_='description')
    
    titles = []
    for item in my_hems_titles:
        titles.append(item.find('h3').text)
    
    img_urls = ['https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg', 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg']
    
    hemisphere_image_urls = [
    {"title": titles[0], "img_url": img_urls[0]},
    {"title": titles[1], "img_url": img_urls[1]},
    {"title": titles[2], "img_url": img_urls[2]},
    {"title": titles[3], "img_url": img_urls[3]},
]
    
    
    my_data = {
        'news_title':news_title,
        'news_p':news_p,
        'featured': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': myfacts_str,
        'img_urls': hemisphere_image_urls
    }
    
    print("Scraping complete")
    
    browser.quit()
    
    return my_data
    
    
    