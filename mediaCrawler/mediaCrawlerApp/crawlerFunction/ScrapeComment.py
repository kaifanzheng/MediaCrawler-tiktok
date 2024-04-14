from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import random

# 您个人的 Chrome 用户数据目录和ChromeDriver路径
user_data_dir = r'/Users/kaifan/Library/Application Support/Google/Chrome'
chrome_driver_path = r'/usr/local/bin/chromedriver'

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
driver = webdriver.Chrome()

def scroll_page(driver, load_times):
    """滚动页面以加载更多内容

    Args:
    driver: WebDriver实例。
    load_times: 要加载的次数。
    """
    for _ in range(load_times):
        # 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("执行加载")
        # 随机等待时间，介于3到7秒之间
        time.sleep(random.uniform(3, 7))

# 访问目标网址
driver.get("https://www.douyin.com/discover?modal_id=7356196656422866239")


def close_popup(driver):
    """
    Function to close the popup window in the Douyin page.
    """
    try:
        # Wait for the close button to be clickable
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dy-account-close"))
        )
        
        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", close_button)
        
        print("Popup closed successfully.")
    except Exception as e:
        print(f"An error occurred while trying to close the popup: {e}")

# 添加您从浏览器中导出的 Cookies
cookies = [
    {'name': 'FOLLOW_LIVE', 'value': '%22MS4wLjABAAAAgUJNYCU4jQB54_461ijiGGqVCmqsWJaQAgwdnXHOo3hrWdNxSK5D5pFmLXj0vwRl%2F1712851200000%2F0%2F1712846712931%2F0%22', 'domain': '.douyin.com', 'path': '/'},
    {'name': 'FORCE_LOGIN', 'value': '%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D', 'domain': '.douyin.com', 'path': '/'},
    {'name': 'IsDouyinActive', 'value': 'true', 'domain': '.douyin.com', 'path': '/'}
]

#for cookie in cookies:
    #driver.add_cookie(cookie)

# 刷新页面以应用 Cookies
driver.refresh()
time.sleep(3)  # 等待一段时间，确保Cookies被正确应用
close_popup(driver)

# 等待评论按钮可点击
comment_button_selector = "#sliderVideo > div.UsWJJZhB.playerContainer.hide-animation-if-not-suport-gpu.jjWFxVjy.dOluRUuw > div.O8onIiBq.slider-video > div > div.MarSXdLE.immersive-player-switch-on-hide-interaction-area.nRO8QGrO.positionBox.hideChangeVideo > div.jkfSVWLT > div:nth-child(3) > div"
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, comment_button_selector))).click()
time.sleep(2)
scroll_page(driver, 3)
time.sleep(10)  # 给页面评论部分加载的时间

# 模拟鼠标移动到屏幕右侧的10%，然后向下滚动20秒

time.sleep(1)
# 现在提取评论的内容
def scrape_user_info_and_comments(driver):
    # 获取当前页面的HTML内容
    page_html = driver.page_source
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # 找到所有评论区域的div
    comments_divs = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["VjrdhTqP"])
    
    # 遍历所有评论以找到需要的信息
    for comment_div in comments_divs:
        # 获取评论文本
        comment_text = comment_div.find("div", class_="LvAtyU_f").get_text(strip=True) if comment_div.find("div", class_="LvAtyU_f") else ""
        
        # 获取用户主页链接 - 现在是评论div中带有 'hY8lWHgA' 类的 'a' 标签的 'href' 属性
        user_profile_tag = comment_div.find("a", class_="hY8lWHgA")
        user_profile_link = "https:" + user_profile_tag['href'] if user_profile_tag and user_profile_tag.has_attr('href') else ""
        
        # 获取用户IP - 假设它是带有 'GOkWHE6S' 类的div中的第一个 'span'
        user_ip_div = comment_div.find("div", class_="GOkWHE6S")
        user_ip = user_ip_div.get_text(strip=True) if user_ip_div else ""
        
        # 打印结果
        print(f"用户评论: {comment_text}")
        print(f"用户主页链接: {user_profile_link}")
        print(f"用户IP: {user_ip}")
        print("---------------------------------------------------")
scrape_user_info_and_comments(driver)
# 关闭浏览器
driver.quit()
