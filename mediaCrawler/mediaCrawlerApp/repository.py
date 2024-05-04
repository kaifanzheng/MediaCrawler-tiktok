from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .models import TikTokUser, LiveStreamVideo, SimilarUser
from .crawlerFunction.DY_liveScraper import get_live_user_name, get_user_queue
import socket
import threading
import queue
import time
from django.db import transaction
import logging
userdata = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
num_thread = 5
db_lock = threading.Lock()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_ip_address():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真的连接，只是用来获取IP
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP

def scrapeTikTokUsers(url):
    tikTokUserQueue = get_live_user_name(url, userdata)
    userlist = list(tikTokUserQueue.queue)
    for username in userlist:
        user = TikTokUser(name=username, ip=get_ip_address())
        user.save()
        



def worker(username_queue):
    while True:
        user = None
        try:
            user = username_queue.get(timeout=10)
            with transaction.atomic():
                # 确保 TikTokUser 已保存
                user.save()  
                result = searchUserByKeyword(3, user.name, userdata, True)
                nicknames, DY_ids = result
                for nickname, dy_id in zip(nicknames, DY_ids):
                    similar_user = SimilarUser(
                        tiktok_user=user,
                        user_id=dy_id,
                        name=nickname,
                        url="https://example.com",
                        ip="192.168.1.2"
                    )
                    similar_user.save()
        except queue.Empty:
            break
        except Exception as e:
            print(f"Error processing user {user.name if user else 'Unknown'}: {e}")
        finally:
            if user:
                username_queue.task_done()
def generate_similar_user_multithread(num_threads):
    username_queue = queue.Queue()

    for user in TikTokUser.objects.all():
        username_queue.put(user)

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(username_queue,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    username_queue.join()

#修改前的版本
# def generateSimilarUser_worker_thread():
#     db_lock.acquire()
#     username_quene = TikTokUser.objects.all()
#     db_lock.release()
#     try:
#         while True:
#             db_lock.acquire()
#             username = username_quene.get()
#             db_lock.release()
#             user = TikTokUser.objects.get(name=username)
#             if username_quene == None:
#                 break
#             result = searchUserByKeyword(3,username,userdata,True)
    
#             for i in range(len(result[0])): 
#                 db_lock.acquire()
#                 similar_user = SimilarUser(
#                     tiktok_user = user,
#                     user_id = result[i][1],
#                     name= result[i][0],
#                     url="https://example.com",
#                     ip="192.168.1.2"
#                 )
#                 similar_user.save()
#                 db_lock.release()
#     finally:
#         print("Driver for thread closed.")

# def generate_similar_user_multithread(num_threads):
#     threads = []
#     for i in range(num_threads):
#         thread = threading.Thread(target=generateSimilarUser_worker_thread)
#         thread.start()
#         threads.append(thread)
#     for thread in threads:
#         thread.join()















# def generateSimilarUsers_muiltithread():
#     #TODO
#     all_users = TikTokUser.objects.all()
#     user_queue = queue.Queue()
# # 将 all_users 存入队列
#     for user in all_users:
#         user_queue.put(user)
    
#     searchResult = generate_similar_user_multithread(user_queue,5)
#     print(searchResult)
#     similar_user = SimilarUser(
#             tiktok_user = user,
#             user_id = searchResult[1],
#             name= searchResult[0],
#             url="https://example.com",
#             ip="192.168.1.2"
#         )
#     similar_user.save()

def findMatchTiktokUser():
    #TODO
    return 0

