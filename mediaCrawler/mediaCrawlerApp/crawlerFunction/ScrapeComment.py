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
import math 

num_scrolls = 0 #计算翻页的次数
# 初始化一个全局变量来跟踪已处理的评论数量
last_processed_comment_count = 0

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

def scroll_comments_section(driver):
    # 等待评论列表容器加载完成
    comments_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.HV3aiR5J.comment-mainContent.iV2CcAAV")))
    # 每次滚动向下移动1000像素
    driver.execute_script(
    'arguments[0].scrollTop = arguments[0].scrollTop + 3200;', 
    comments_container
        )
    # 每次滚动之间等待3到7秒的随机时间
    time.sleep(random.randint(3, 7))


def calculate_pagination(driver):
    """
    计算需要翻页的次数，并作为整数返回。
    """
    try:
        total_comments_text = driver.find_element(By.CSS_SELECTOR, "span.qx5s_hbj").text
        total_comments = int(total_comments_text.split('(')[1].split(')')[0])
        print(f"全部评论数量: {total_comments}")
        
        comments_per_page = 19
        total_pages = math.ceil(total_comments / comments_per_page)
        print(f"需要翻页的次数: {total_pages}")
        return total_pages
        
    except Exception as e:
        print(f"获取评论总数时出现错误: {e}")
        return 0
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

# 为用户编写一个Selenium脚本的函数，用于点击评论区域的登录遮罩关闭按钮。
def click_comment_login_mask(driver):
    try:
        # 等待遮罩的关闭按钮出现
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".related-video-card-login-guide__footer-close"))
        )
        
        # 点击关闭按钮
        close_button.click()
        print("已点击评论区的登录遮罩关闭按钮。")
        
    except Exception as e:
        print(f"不执行关闭登录遮罩")

def click_comments_button(driver):
    comment_button_selector = "#sliderVideo > div.UsWJJZhB.playerContainer.hide-animation-if-not-suport-gpu.jjWFxVjy.dOluRUuw > div.O8onIiBq.slider-video > div > div.MarSXdLE.immersive-player-switch-on-hide-interaction-area.nRO8QGrO.positionBox.hideChangeVideo > div.jkfSVWLT > div:nth-child(3) > div"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, comment_button_selector))).click()
    print("点击评论")
    time.sleep(2)

def scrape_user_info_and_comments(driver):
    global last_processed_comment_count  # 引用全局变量
    # 获取当前页面的HTML内容
    page_html = driver.page_source
    
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # 找到所有评论区域的div
    comments_divs = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["VjrdhTqP"])
    print(f"当前加载的评论数量: {len(comments_divs)}")
    # 遍历所有评论以找到需要的信息

    new_comments = comments_divs[last_processed_comment_count:] 
    for comment_div in new_comments:
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
    last_processed_comment_count += len(new_comments)



def scrape_user_info_from_video(driver,url):
    driver.get(url)
    time.sleep(3)  
    close_popup(driver)
    click_comments_button(driver)
    click_comment_login_mask(driver)
    num_scrolls = calculate_pagination(driver)
    for current_scroll in range(num_scrolls):
        remaining_scrolls = num_scrolls - current_scroll - 1  # 计算剩余翻页次数
        print(f"当前加载次数: {current_scroll + 1}, 剩余加载次数: {remaining_scrolls}")
        scroll_comments_section(driver)  # 假设这个函数用来滚动到评论区的下一部分
        time.sleep(3)  # 给页面评论部分加载的时间
        scrape_user_info_and_comments(driver)  # 爬取并打印当前页的评论
    driver.quit()
# 关闭浏览器

#scrape_user_info_from_video(driver,"https://www.douyin.com/discover?modal_id=7356196656422866239")

