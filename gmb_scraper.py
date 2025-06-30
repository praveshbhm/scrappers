import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import tempfile
import os

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Change path as needed; use chromedriver in system PATH or downloaded location
    service = Service('./chromedriver')  # or full path like '/usr/bin/chromedriver'
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_gmb(query):
    driver = init_driver()
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(4)

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

# ------------------ Streamlit App ------------------

st.title("🔍 GMB Scraper Tool")
st.markdown("Enter a business name and location (e.g., `Urban Lube Calgary`) to fetch public details from Google Search.")

query = st.text_input("Enter Business Name with City", "")

if st.button("Scrape"):
    if query:
        with st.spinner("Scraping GMB info..."):
            result = scrape_gmb(query)
            df = pd.DataFrame([result])
            st.success("Scraping completed!")
            st.dataframe(df)

            # Download CSV
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
                df.to_csv(tmpfile.name, index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=open(tmpfile.name, 'rb').read(),
                    file_name='gmb_data.csv',
                    mime='text/csv'
                )
                os.unlink(tmpfile.name)
    else:
        st.warning("Please enter a business name.")
