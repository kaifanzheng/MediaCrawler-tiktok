from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
# 用户个人的 Chrome 用户数据目录和ChromeDriver路径
user_data_dir = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
chrome_driver_path = r'C:\Users\Administrator\Desktop\chromedriver-win64\chromedriver.exe'

# 配置 Chrome 浏览器选项
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
#chrome_options.add_argument("--headless")  # 无头模式

# 设置 ChromeDriver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 访问指定网址
live_url = "https://live.douyin.com/92671200827?column_type=single&is_aweme_tied=0&search_id=2024041522444608FD86F712A39222C5F7&search_result_id=7358060145957539106"
  # 此处将网址定义为变量，以便于在代码编辑器中修改
driver.get(live_url)

def close_popup(driver):
    """
    优化版：尝试关闭抖音页面上的弹窗，如果弹窗不存在则安静地跳过。
    """
    try:
        # 检查弹窗关闭按钮是否存在
        close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dy-account-close"))
        )
        if close_button:
            # 如果按钮存在，则使用JavaScript点击关闭按钮
            driver.execute_script("arguments[0].click();", close_button)
            print("弹窗已成功关闭。")
    except Exception as e:
        # 如果在尝试查找元素时出现异常，则认为弹窗不存在，不打印错误信息
        print("没有检测到弹窗，继续执行程序。")

def fetch_comments(driver):
    last_seen_comment_id = None
    try:
        while True:
            # 获取当前所有评论元素
            comments = driver.find_elements(By.CSS_SELECTOR, "#chatroom > div > div.rXSKGskq > div.h02Ml9ry > div > div > div > div.webcast-chatroom___item-offset > div > div:nth-child(1) > div")
            if comments:
                current_last_comment_id = comments[-1].get_attribute("data-id")

            new_comments = []
            if last_seen_comment_id is not None:
                index_of_last_seen = next((i for i, comment in enumerate(comments) if comment.get_attribute("data-id") == last_seen_comment_id), None)
                if index_of_last_seen is not None and index_of_last_seen + 1 < len(comments):
                    new_comments = comments[index_of_last_seen + 1:]

            if comments:
                last_seen_comment_id = current_last_comment_id

            for comment in new_comments:
                try:
                    username_elem = comment.find_element(By.CSS_SELECTOR, "span.u2QdU6ht")
                    content_elem = comment.find_element(By.CSS_SELECTOR, "span.WsJsvMP9")
                    username = username_elem.text.split('：')[0]
                    content = content_elem.text
                    print(f"评论用户: {username}, 评论内容: {content}, 爬取时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                except StaleElementReferenceException:
                    print("被反爬")
                except Exception as e:
                    print("被反爬", e)

            time.sleep(0.5)  # 每1秒检查一次新评论
    except Exception as e:
        print(f"被反爬: {e}")





close_popup(driver)
# 注释调用fetch_comments函数，以免在PCI中运行
fetch_comments(driver)
