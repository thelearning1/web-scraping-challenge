# Mission to Mars
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# driver = webdriver.Chrome(executable_path='chromedriver.exe')


def scrape():

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the mars news site
    url = "https://redplanetscience.com"

    #navigate to the site and pull the html
    browser.visit(url)
    html = browser.html

    time.sleep(1)

    #create the soup
    soup = bs(html,"html.parser")

    #isolate the places where the correct info can be found and bind them to the variables
    news_title = soup.find_all('div',class_="content_title")
    news_p = soup.find_all('div',class_="article_teaser_body")
    news_p = news_p[0].text
    news_title = news_title[0].text

    #navigate to site hosting the image
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    time.sleep(1)

    #rummage through the soup the soup to pull the image source
    html = browser.html
    soup = bs(html,"html.parser")

    #get the url portion from the header image and create full url
    image = soup.find("img",class_="headerimage fade-in")['src']
    image_url = f"{url}/{image}"

    #navigate to the third site that has mars facts
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)

    time.sleep(1)

    #rummage through the soup the soup to pull the image source
    html = browser.html
    mars_table = pd.read_html(url)
    mars_table_string = mars_table[1].to_html(index=False,header=False)

    #navigate to the site that has the images of the martian hemispheres
    url = "https://marshemispheres.com"
    browser.visit(url)
    html = browser.html
    soup = bs(html,'html.parser')

    time.sleep(1)

    #pull the hemisphere names out of the links
    hemispheres = []
    n = 0
    for h3 in soup.find_all('h3'):
        if n < 4:
            x = h3.get_text().split(' En')[0]
            hemispheres.append(x)
            n+=1

    #create a list of links for navigation
    tnail_links = []
    for result in soup.find_all('div',class_='collapsible results'):
        for anchor in result.find_all('a'):
            if (anchor.img):
                tnail_links.append(f'{url}/{anchor["href"]}')

    #go to each page in the list to pull the full-size images
    links = []
    for tnail in tnail_links:
        browser.visit(tnail)
        time.sleep(1)
        html = browser.html
        soup = bs(html,'html.parser')
        
        #find the images in the soup and put the links in the list
        result = soup.find_all('img',class_='wide-image')
        extension = result[0]['src']
        links.append(f'{url}/{extension}')

    # Zip some tuples of the 
    hemizip = zip(hemispheres, links)
    dict_list = []

    # Iterate through the zipped object
    for title, img in hemizip:
        mars_dict = {}
        
        # Add title key
        mars_dict['title'] = title
        
        # Add url key
        mars_dict['img_url'] = img
        
        # put dictionaries in the list
        dict_list.append(mars_dict)

    #compile everything into a single dictionary
    scraped_data = {
        "News_Headline":news_title,
        "News_Content":news_p,
        "Main_Image":image_url,
        "Mars_Table":mars_table_string,
        "Hemispheres":dict_list
    }

    #close the browser
    browser.quit()

    #return the scraped dictionary
    return scraped_data