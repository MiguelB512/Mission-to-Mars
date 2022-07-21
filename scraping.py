# # Web Scraping section

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things

# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
# As an example, ul.item_list would be found in HTML as <ul class="item_list">.

# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is 
# useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.



def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# Image scraping section

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

# Create a function to scrape the mars hemisphere photos

def hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # Get list of all hemisphere links 
    links = browser.find_by_css('a.product-item img')

    # Loop through links, click on them, and retrieve the href for each link 
    for i in range(len(links)):
        
        # Create results dictionary that holds our findings 
        hemispheres = {}

        # Find anchors with product-item and click on them for each i 
        browser.find_by_css('a.product-item img')[i].click()

        # Find the Sample image anchor tag and get the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemispheres['img_url'] = sample_elem["href"]
        
        # Get Hemisphere title
        hemispheres['title'] = browser.find_by_css('h2.title').text
        
        # Add hemisphere information to hemisphere_image_urls 
        hemisphere_image_urls.append(hemispheres)
        
        # Tell the browser to navigate back so that the next section of the loop can begin
        browser.back()


    return(hemisphere_image_urls)
