from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service('./chromedriver')  # Path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_gmb(query):
    driver = init_driver()
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(4)  # wait for page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    try:
        name = soup.select_one('.SPZz6b span').text.strip()
    except:
        name = 'N/A'
        
    try:
        rating = soup.select_one('span.Aq14fc').text.strip()
    except:
        rating = 'N/A'
        
    try:
        reviews = soup.select_one('span.EBe2gf').text.strip()
    except:
        reviews = 'N/A'
        
    try:
        address = soup.select_one('span.LrzXr').text.strip()
    except:
        address = 'N/A'
        
    try:
        phone = soup.select_one('span.LrzXr.zdqRlf.kno-fv').text.strip()
    except:
        phone = 'N/A'
    
    try:
        website = soup.find('a', attrs={'data-attrid': 'website'})['href']
    except:
        website = 'N/A'

    driver.quit()

    return {
        'Name': name,
        'Rating': rating,
        'Reviews': reviews,
        'Address': address,
        'Phone': phone,
        'Website': website
    }

if __name__ == "__main__":
    queries = [
        "Urban Lube Calgary",
        "Prince Tires Calgary",
        "Batteries Store Regina"
    ]
    
    data = []
    for q in queries:
        print(f"Scraping: {q}")
        result = scrape_gmb(q)
        data.append(result)

    df = pd.DataFrame(data)
    df.to_csv("gmb_scraped_data.csv", index=False)
    print("Scraping completed. Data saved to gmb_scraped_data.csv.")
