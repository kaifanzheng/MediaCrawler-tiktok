# import threading
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import queue
# import time
# import random
# import string
# import os
# import tempfile
# from .DY_liveScraper import get_user_queue


# user_data_dir = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'

# def scroll_page(driver, load_times):
#     for _ in range(load_times):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(3, 7))


# def get_random_user_agent():
#     # 列表中可以添加更多的 User-Agent
#     user_agents = [
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
#         "Mozilla/5.0 (iPad; CPU OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1"
#     ]
#     return random.choice(user_agents)

# def driver_setup(user_data_dir):
#     user_data_dir = tempfile.mkdtemp()  # 创建一个临时目录用作用户数据目录
#     chrome_driver_path = r'C:\Users\Administrator\Desktop\chromedriver-win64\chromedriver.exe'
#     chrome_options = Options()
#     chrome_options.add_argument(f"user-data-dir={user_data_dir}")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--disable-plugins-discovery")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     service = Service(executable_path=chrome_driver_path)
#     return webdriver.Chrome(service=service, options=chrome_options)


# def searchUserByKeyword(scrollPage, keyword, userdata,log):
#     driver = driver_setup(userdata)
#     nicknames = []
#     DY_ids = []
#     try:
#         # Record start time
#         start_time = time.time()

#         # Construct search result URL and visit
#         driver.get(f"https://www.douyin.com/search/{keyword}?type=user")
        
#         scroll_page(driver,scrollPage)
#         # Wait for the page to load completely, adjust wait time as necessary
#         driver.implicitly_wait(10)

#         # Extract all users' nicknames and Douyin IDs
#         users = driver.find_elements(By.XPATH, '//li[contains(@class, "MgWTwktU")]')
#         for user in users:
#             # Nickname
#             nickname = user.find_element(By.XPATH, './/div[contains(@class, "_HB0BapG")]/p').text
#             # Douyin ID
#             douyin_id_elements = user.find_elements(By.XPATH, './/div[contains(@class, "H7Xy0nwI")]/span')
#             douyin_id = [elem.text for elem in douyin_id_elements if elem.text.startswith('抖音号')][0].replace('抖音号: ', '')
#             if(log == True):
#                 print(f'Nickname: {nickname}, Douyin ID: {douyin_id}')
#             nicknames.append(nickname)
#             DY_ids.append(douyin_id)

#         # Record end time
#         end_time = time.time()
#         if(log == True):
#             print(f"Program run time: {end_time - start_time} seconds")

#     finally:
#         # Cleanup: close the browser window
#         driver.quit()
#         return [nicknames,DY_ids]

# # def worker_thread():
# #     username_quene = get_user_queue()
# #     try:
# #         while not username_quene.empty():
# #             username = username_quene.get_nowait()
# #             user = TikTokUser.objects.get(name=username)
# #             result = searchUserByKeyword(3,username,user_data_dir,True)
# #             for i in range(len(result[0])):
                
# #     finally:
# #         print("Driver for thread closed.")




# def generate_similar_user_multithread(queue, num_threads):
#     results = []
#     threads = []
#     for i in range(num_threads):
#         thread = threading.Thread(target=worker_thread, args=(queue, results))
#         thread.start()
#         threads.append(thread)
#     for thread in threads:
#         thread.join()

#     # Print all results collected
#     for result in results:
#         print(result)


# # def generate_test_queue(num_users):
# #     test_queue = queue.Queue()
# #     for _ in range(num_users):
# #         username = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 3)))
# #         test_queue.put(username)
# #     return test_queue


# # def test_multithreading_with_queue(num_threads, num_users):
# #     test_queue = generate_test_queue(num_users)
# #     results = []
# #     threads = []
# #     for i in range(num_threads):
# #         thread = threading.Thread(target=worker_thread, args=(test_queue, results))
# #         thread.start()
# #         threads.append(thread)
# #     for thread in threads:
# #         thread.join()

# #     # Print all results collected
# #     for result in results:
# #         print(result)

# # if __name__ == "__main__":
# #     start_time = time.time()
# #     num_threads = 1 
# #     num_users = 10
# #     test_multithreading_with_queue(num_threads, num_users)
# #     end_time = time.time()
# #     print(f"Time taken for {num_threads} threads: {end_time - start_time} seconds")
