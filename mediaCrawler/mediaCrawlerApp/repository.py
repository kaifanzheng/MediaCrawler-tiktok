from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .models import TikTokUser, LiveStreamVideo, SimilarUser
from .crawlerFunction.DY_liveScraper import get_live_user_name, get_user_queue
import socket
from threading import Thread, Lock
import queue
import time
from django.db import transaction
import logging


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
    tikTokUserQueue = get_live_user_name(url)
    userlist = list(tikTokUserQueue.queue)
    for username in userlist:
        user = TikTokUser(name=username, ip=get_ip_address())
        user.save()


def initializeSimilarUsers(tiktok_user, user_dict, lock):
    with transaction.atomic():
        result = searchUserByKeyword(2, tiktok_user.name, True)
        with lock:
            user_dict[tiktok_user] = result

def generateSimilarUsers():
    non_assigned_users = TikTokUser.objects.filter(is_searched=False)
    user_dict = {user: None for user in non_assigned_users}
    lock = Lock()  # Create a lock object
    threads = []

    for user in non_assigned_users:
        thread = Thread(target=initializeSimilarUsers, args=(user, user_dict, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return user_dict

def findMatchTiktokUser():
    #TODO
    return 0

