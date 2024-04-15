from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

# 定义浏览器配置和路径
def configure_browser():
    user_data_dir = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
    chrome_driver_path = r'C:\Users\Administrator\Desktop\chromedriver-win64\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def close_popup(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".dy-account-close")))
        driver.execute_script("arguments[0].click();", close_button)
        print("弹窗已成功关闭。")
    except TimeoutException:
        print("没有检测到弹窗，继续执行程序。")

def fetch_comments(driver):
    last_seen_comment_id = None
    try:
        while True:
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
        print(f"异常停止: {e}")

def display_comment(comment):
    try:
        username_elem = comment.find_element(By.CSS_SELECTOR, "span.u2QdU6ht")
        content_elem = comment.find_element(By.CSS_SELECTOR, "span.WsJsvMP9")
        username = username_elem.text.split('：')[0]
        content = content_elem.text
        print(f"评论用户: {username}, 评论内容: {content}, 爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    except StaleElementReferenceException:
        print("被反爬")
    except Exception as e:
        print("评论处理异常", e)

# 主函数
def main():
    driver = configure_browser()
    live_url = "https://live.douyin.com/249658474606?is_aweme_tied=0"
    driver.get(live_url)
    close_popup(driver)
    fetch_comments(driver)

if __name__ == "__main__":
    main()
