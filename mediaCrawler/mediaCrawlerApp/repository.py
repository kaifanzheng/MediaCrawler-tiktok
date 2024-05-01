from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .models import TikTokUser, LiveStreamVideo, SimilarUser
from .crawlerFunction.DY_liveScraper import get_live_user_name, get_user_queue
import socket
from.crawlerFunction.generate_similar_user_multithread import generate_similar_user_multithread
import threading

userdata = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'
num_thread = 10

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

def scrapeTikTikUsers(url):
    tikTokUserQueue = get_live_user_name(url,userdata)

    while True:
        if tikTokUserQueue.empty():
            break 
        username = tikTokUserQueue.get()
        user = TikTokUser(name=username, ip=get_ip_address())
        user.save()

def generateSimilarUser_worker_thread():
    username_quene = get_user_queue()
    try:
        while not username_quene.empty():
            username = username_quene.get_nowait()
            user = TikTokUser.objects.get(name=username)
            result = searchUserByKeyword(3,username,userdata,True)
            for i in range(len(result[0])): 
                similar_user = SimilarUser(
                    tiktok_user = user,
                    user_id = result[i][1],
                    name= result[i][0],
                    url="https://example.com",
                    ip="192.168.1.2"
                )
                similar_user.save()
    finally:
        print("Driver for thread closed.")

def generate_similar_user_multithread(queue, num_threads):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=generateSimilarUser_worker_thread)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

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

