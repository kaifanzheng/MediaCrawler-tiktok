from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

def scroll_page(driver, load_times):
    """Scrolls the page to load more content.

    Args:
        driver: An instance of WebDriver.
        load_times: The number of times to load more content.
    """
    for _ in range(load_times):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Loading executed")
        # Random wait time between 3 and 7 seconds
        time.sleep(random.uniform(3, 7))

def driverSetup(user_data_dir):
    # Assuming 'driver' is an already initialized WebDriver object
    # Example usage: scroll_page(driver, 5) # Scrolls the page 5 times

    # User data and Chrome driver path

    # Configuration of Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initializing the WebDriver
    driver = webdriver.Chrome()
    return driver

# Functionality to get video by keyword
def searchVideoByKeyword(scrollPage, keyword, log):
    driver = driverSetup(r'/Users/kaifan/Library/Application Support/Google/Chrome')
    scroll_page(driver, scrollPage)

    try:
        # Record start time
        start_time = time.time()

        # Construct search result URL and visit
        driver.get(f"https://www.douyin.com/search/{keyword}?type=video")

        # Wait for the page to fully load
        driver.implicitly_wait(10)
        scroll_page(driver, 3)  # Scroll 3 times to load more content

        # Extract information from all videos
        videos = driver.find_elements(By.CSS_SELECTOR, 'li[class*="MgWTwktU"]')
        for video in videos:
            # Tags
            tags = video.find_element(By.CSS_SELECTOR, 'div[class="swoZuiEM"]').text
            # Video link
            video_link_element = video.find_element(By.CSS_SELECTOR, 'a[class="B3AsdZT9 AqS8FEQL"]')
            video_link = f"https:{video_link_element.get_attribute('href')}"
            # Like count
            like_count = video.find_element(By.CSS_SELECTOR, 'span[class="IcU0dfgd"]').text
            # Publish time
            publish_time = video.find_element(By.CSS_SELECTOR, 'span[class="bu9WFx2P"]').text
            if(log == True):
                print(f'Tags: {tags}, Video Link: {video_link}, Likes: {like_count}, Published: {publish_time}')

        # Record end time
        end_time = time.time()
        if(log == True):
            print(f"Program run time: {end_time - start_time} seconds")

    finally:
        # Clean up: close the browser window
        driver.quit()
        return [tags,video_link]

def searchUserByKeyword(scrollPage, keyword, log):
    driver = driverSetup(r'/Users/kaifan/Library/Application Support/Google/Chrome')
    try:
        # Record start time
        start_time = time.time()

        # Construct search result URL and visit
        driver.get(f"https://www.douyin.com/search/{keyword}?type=user")
        
        scroll_page(driver,scrollPage)
        # Wait for the page to load completely, adjust wait time as necessary
        driver.implicitly_wait(10)

        # Extract all users' nicknames and Douyin IDs
        users = driver.find_elements(By.XPATH, '//li[contains(@class, "MgWTwktU")]')
        for user in users:
            # Nickname
            nickname = user.find_element(By.XPATH, './/div[contains(@class, "_HB0BapG")]/p').text
            # Douyin ID
            douyin_id_elements = user.find_elements(By.XPATH, './/div[contains(@class, "H7Xy0nwI")]/span')
            douyin_id = [elem.text for elem in douyin_id_elements if elem.text.startswith('抖音号')][0].replace('抖音号: ', '')
            if(log == True):
                print(f'Nickname: {nickname}, Douyin ID: {douyin_id}')

        # Record end time
        end_time = time.time()
        if(log == True):
            print(f"Program run time: {end_time - start_time} seconds")

    finally:
        # Cleanup: close the browser window
        driver.quit()
        return [nickname,douyin_id]
