from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import queue


stopScrapperFlag = 0
chrome_driver_path = r'/Users/kaifan/Library/Application Support/Google/Chrome'
# 创建一个先进先出的队列
user_name_queue = queue.Queue(maxsize=100000)  # maxsize是可选参数，用来设置队列可以容纳的最大元素数量，0或负值表示无大小限制


limited_time = 40 #爬取评论的程序每次运行的时间



# 定义浏览器配置和路径
def configure_browser(user_data_dir):
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    return webdriver.Chrome()

def close_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dy-account-close")))
        driver.execute_script("arguments[0].click();", close_button)
        print("弹窗已成功关闭。")
    except TimeoutException:
        print("没有检测到弹窗，继续执行程序。")

def setFlagToStop():
    global stopScrapperFlag
    stopScrapperFlag = 1
def setFlagToStart():
    global stopScrapperFlag
    stopScrapperFlag = 0

def fetch_comments(driver):
    last_seen_comment_id = None
    start_time = time.time()

    try:
        while True:
            current_time = time.time()
            if current_time - start_time > limited_time:
                break
            if stopScrapperFlag == 1:
                break
            comments = driver.find_elements(By.CSS_SELECTOR, "#chatroom > div > div.rXSKGskq > div.h02Ml9ry > div > div > div > div.webcast-chatroom___item-offset > div > div:nth-child(1) > div")
            new_comments = []
            if comments:
                current_last_comment_id = comments[-1].get_attribute("data-id")
                if last_seen_comment_id is not None:
                    index_of_last_seen = next((i for i, comment in enumerate(comments) if comment.get_attribute("data-id") == last_seen_comment_id), None)
                    if index_of_last_seen is not None and index_of_last_seen + 1 < len(comments):
                        new_comments = comments[index_of_last_seen + 1:]
                if comments:
                    last_seen_comment_id = current_last_comment_id
                for comment in new_comments:

                    display_comment(comment)
            time.sleep(0.5)
    except Exception as e:
        print(f"检测到反爬: {e}")

def display_comment(comment):
    try:
        
        username_elem = comment.find_element(By.CSS_SELECTOR, "span.u2QdU6ht")
        #content_elem = comment.find_element(By.CSS_SELECTOR, "span.WsJsvMP9")
        username = username_elem.text.split('：')[0]
        #content = content_elem.text
        print(f"评论用户: {username}")
        user_name_queue.put(username)
    except StaleElementReferenceException:
        print("被反爬")
    except Exception as e:
        print("评论处理异常", e)

#method that project queue        
def get_user_queue():
    return user_name_queue

def empty_user_queue():
    user_name_queue = queue.Queue(maxsize=100000)

# 主函数
def get_live_user_name(live_url):
    driver = configure_browser(chrome_driver_path)
    driver.get(live_url)
    close_popup(driver)
    fetch_comments(driver)
    return get_user_queue()

