# import dependencies
from splinter import Browser
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import time

def init_browser():
    # Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}
hemisphere_image_urls = []



    # Mars News
# mars_news = {}
# mars_image=()
# mars_weath=()
# mars_facts=[]
# mars_hemps=[]

def marsnews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find("div", class_='list_text')

    mars_data["news_title"] = article.find("div", class_="content_title").text
    mars_data["news_p"] = article.find("div", class_ ="article_teaser_body").text
    mars_data["latest_news_date"] = (soup.find_all('div', class_="list_date"))[0].get_text()

    browser.quit()

    return mars_data

   
        
# Mars Image
def marsimage():
    browser = init_browser()

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    
    mars_data["featured_image_url"] = "https://www.jpl.nasa.gov" + image
    browser.quit()

    return mars_data


# Mars Weather
def marsweather():
    browser = init_browser()

    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)   
    html = browser.html
    tweet_soup = bs(html, 'html.parser')

    mars_data["mars_weather"] = tweet_soup.find('div',class_="css-1dbjc4n").get_text()

    browser.quit()

    return mars_data


# # Mars Facts
def marsfacts():
    browser = init_browser()

    mars_facts_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(mars_facts_url)
    mars_df = mars_table[0]
    mars_df.columns = ["Facts", "Value"]
    mars_df.set_index(["Facts"])
    mars_facts_html = mars_df.to_html()
    
    mars_data["mars_facts_html"] = mars_facts_html.replace("\n","")
    browser.quit()
    return mars_data
    

# Mars Hemispheres
def marshemp():
    browser = init_browser()

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    nextpage_urls = []
    imgtitles = []
    base_url = 'https://astrogeology.usgs.gov'
    html = browser.html
    soup = bs(html, 'html.parser')
    divs = soup.find_all('div', class_='description')
    
    counter = 0
    for div in divs:
        link = div.find('a')
        href=link['href']
        img_title = div.a.find('h3')
        img_title = img_title.text
        imgtitles.append(img_title)
        next_page = base_url + href

        nextpage_urls.append(next_page)
        counter = counter+1

        if (counter == 4):
            break

        my_images=[]
        for nextpage_url in nextpage_urls:
            url = nextpage_url
            browser.visit(url)
            html = browser.html
            soup = bs(html, 'html.parser')
            link2 = soup.find('img', class_="wide-image")
            forfinal = link2['src']
            full_img = base_url + forfinal
            my_images.append(full_img)
            nextpage_urls = []


        # hemisphere_image_urls = []

        cerberus = {'title':imgtitles[0], 'img_url': my_images[0]}
        schiaparelli = {'title':imgtitles[1], 'img_url': my_images[1]}
        syrtis = {'title':imgtitles[2], 'img_url': my_images[2]}
        valles = {'title':imgtitles[3], 'img_url': my_images[3]}

        mars_data["hemisphere_image_urls"] = [cerberus, schiaparelli, syrtis, valles]
        browser.quit()

        return mars_data

      




