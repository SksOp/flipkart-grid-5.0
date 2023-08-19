from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import os
import time
from constants.social_media import links


def scrapper(checkpoint=0):
    # Set up the path where you want to save the images
    save_path = "data/temp/scrapped"
    min_size = 10 * 1024  # Minimum file size in bytes (10 KB)

    # Create the directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Created directory: {save_path}")

    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    print(f"WebDriver set up with options: {options.arguments}")

    # Function to handle network errors and connection timeouts

    def retry_request(url, max_retries=5, delay=20):
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying in {delay} seconds...")
                retries += 1
                time.sleep(delay)
        raise Exception(
            f"Failed to retrieve {url} after {max_retries} retries.")

    # Function to scroll down the page and load more images

    def scroll_page(driver, scrolls=2, delay=5):
        for i in range(scrolls):
            try:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                print(f"Scrolled page {i+1}/{scrolls}")
                time.sleep(delay)  # Wait for the images to load
            except Exception as e:
                print(f"Error while scrolling: {e}")

    # List of phrases to search
    phrases = ['Kids', 'Women Western', 'Women Tops', 'Women Dresses', 'Women Jeans', 'Track Pants', 'Women Ethnic', 'Women Sarees', 'Women Kurtis', 'Men Jeans', 'Men Trousers', 'Men Shorts',
               'Men Cargos', 'Men Lowers', 'Men Ethnic', 'Men T-Shirts', 'Men Casual Shirts', 'Men Formal Shirts', 'Men Kurtas', 'Men Blazers', 'Girls Dresses', 'Ethnic Dresses', 'Men Top Wear']

    # Search for each phrase with the word "trending" and download the images
    for phrase in phrases:
        search_query = f"{phrase} trending"
        search_query = search_query.replace(' ', '%20')
        urls = [link.replace("{search_query}", search_query) for link in links]
        print(f"Searching for: {search_query}")
        for url in urls:
            # Load the page and scroll down
            try:
                print(f"Loading page: {url}")
                driver.get(url)
                scroll_page(driver)
            except Exception as e:
                print(f"Error while loading the page: {e}")

            # Get the page source and create a BeautifulSoup object
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find all the img tags
            img_tags = soup.find_all("img")
            print(f"Found {len(img_tags)} img tags")

            # Download the images
            for img_tag in img_tags:
                try:
                    img_url = img_tag["src"]
                    img_name = os.path.basename(img_url)
                    img_path = os.path.join(save_path, img_name)
                    with open(img_path, "wb") as f:
                        f.write(retry_request(img_url).content)
                    # Check the file size and delete small images
                    if os.path.getsize(img_path) < min_size:
                        os.remove(img_path)
                        print(f"Deleted image smaller than 10 KB: {img_url}")
                    else:
                        print(f"Downloaded image: {img_url}")
                except Exception as e:
                    print(f"Error while downloading {img_url}: {e}")

    # Close the WebDriver
    driver.close()
    print("WebDriver closed")
