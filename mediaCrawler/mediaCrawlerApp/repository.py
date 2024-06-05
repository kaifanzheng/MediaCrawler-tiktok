from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .crawlerFunction.DY_liveScraper import get_live_user_name, get_user_queue,empty_user_queue
from threading import Thread, Lock
from django.db import transaction

tikTokUserQueue = None
user_dict = {}
results = []

def scrapeTikTokUsers(url):
    get_live_user_name(url)
    tikTokUserQueue = get_user_queue

def initializeSimilarUsers(tiktok_user, lock):
    with transaction.atomic():
        result = searchUserByKeyword(2, tiktok_user, True)
        with lock:
            user_dict[tiktok_user] = result

def generateSimilarUsers():
    while not tikTokUserQueue.empty():
        username = tikTokUserQueue.get()
        user_dict[username] = None
    lock = Lock()  # Create a lock object
    threads = []

    for user in user_dict.keys():
        thread = Thread(target=initializeSimilarUsers, args=(user, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def findMatchTiktokUser():
    for key in user_dict.keys():
        results.append(user_dict[key][1][0])
def getReuslts():
    return results
def emptyData():
    empty_user_queue()
    tikTokUserQueue = None
    user_dict = {}
    results = []