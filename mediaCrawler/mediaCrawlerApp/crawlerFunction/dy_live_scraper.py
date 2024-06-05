# mediaCrawler/crawlerFunction/dy_live_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import threading

chrome_driver_path = r'/Users/kaifan/Library/Application Support/Google/Chrome'
limited_time = 1000  # 爬取评论的程序每次运行的时间

# 确保爬虫功能模块有一个全局变量来控制爬虫的运行状态
running = True

# 定义浏览器配置和路径
def configure_browser(user_data_dir):
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    return webdriver.Chrome(options=chrome_options)

def close_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dy-account-close")))
        driver.execute_script("arguments[0].click();", close_button)
        print("弹窗已成功关闭。")
    except TimeoutException:
        print("没有检测到弹窗，继续执行程序。")

def fetch_comments(driver):
    last_seen_comment_id = None
    start_time = time.time()
    channel_layer = get_channel_layer()

    def send_user_to_frontend(username):
        print(f"Sending username to WebSocket: {username}")
        async_to_sync(channel_layer.group_send)(
            "users",
            {
                "type": "user_message",
                "message": username,
            }
        )
        print(f"Username {username} sent to WebSocket")

    global running
    try:
        while running:
            current_time = time.time()
            if current_time - start_time > limited_time:
                break
            try:
                comments = driver.find_elements(By.CSS_SELECTOR, ".webcast-chatroom___item")
                if comments:
                    current_last_comment_id = comments[-1].get_attribute("data-id")
                    if last_seen_comment_id is not None:
                        index_of_last_seen = next((i for i, comment in enumerate(comments) if comment.get_attribute("data-id") == last_seen_comment_id), None)
                        if index_of_last_seen is not None and index_of_last_seen + 1 < len(comments):
                            comments = comments[index_of_last_seen + 1:]
                    if comments:
                        last_seen_comment_id = current_last_comment_id
                    for comment in comments:
                        try:
                            username_elem = comment.find_element(By.CSS_SELECTOR, "span.u2QdU6ht")
                            username = username_elem.text.split('：')[0]
                            print(f"评论用户: {username}")
                            send_user_to_frontend(username)
                        except (StaleElementReferenceException, NoSuchElementException) as e:
                            print(f"评论处理异常: {e}")
                            continue  # 继续处理下一条评论
            except StaleElementReferenceException:
                pass
            time.sleep(0.5)
    except Exception as e:
        print(f"检测到反爬: {e}")

# 主函数
def test_get_live_user_name(live_url):
    global running
    running = True
    print(f"Starting to scrape live URL: {live_url}")
    driver = configure_browser(chrome_driver_path)
    driver.get(live_url)
    close_popup(driver)
    fetch_comments(driver)
    driver.quit()

def start_scrape(live_url):
    thread = threading.Thread(target=test_get_live_user_name, args=(live_url,))
    thread.start()

def stop_scraping_function():
    global running
    running = False
