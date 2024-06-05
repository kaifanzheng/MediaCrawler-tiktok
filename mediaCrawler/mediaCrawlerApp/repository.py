from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .crawlerFunction.DY_liveScraper import get_live_user_name, get_user_queue,empty_user_queue
from threading import Thread, Lock
from django.db import transaction
from queue import Queue

class TikTokUserScraper:
    def __init__(self):
        self.tikTokUserQueue = Queue()
        self.user_dict = {}
        self.results = []
        self.url = ''
        self.lock = Lock()

    def scrapeTikTokUsers(self):
        get_live_user_name(self.url)
        self.tikTokUserQueue = get_user_queue()

    def initializeSimilarUsers(self, tiktok_user):
        with transaction.atomic():
            result = searchUserByKeyword(2, tiktok_user, True)
            with self.lock:
                self.user_dict[tiktok_user] = result

    def generateSimilarUsers(self):
        while not self.tikTokUserQueue.empty():
            username = self.tikTokUserQueue.get()
            self.user_dict[username] = None

        threads = []

        for user in self.user_dict.keys():
            thread = Thread(target=self.initializeSimilarUsers, args=(user,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def findMatchTiktokUser(self):
        for key in self.user_dict.keys():
            self.results.append(self.user_dict[key][1][0])

    def getResults(self):
        return self.results

    def setUrl(self, inputUrl):
        self.url = inputUrl

    def emptyData(self):
        self.tikTokUserQueue = Queue()
        self.user_dict = {}
        self.results = []
        self.url = ''