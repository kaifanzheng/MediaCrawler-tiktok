from django.test import TestCase
from .repository import *
from .crawlerFunction.DY_liveScraper import get_live_user_name, setFlagToStop, setFlagToStart,stopScrapperFlag

import threading
import time
class TikTokUserTest(TestCase):
    def test_search_silmilar_users (self):
        setFlagToStart()
        scraperRepo = TikTokUserScraper()
        def run_scraper():
            scraperRepo.scrapeTikTokUsers()
        scraperRepo.setUrl("https://live.douyin.com/36124510415")
        threading.Thread(target=run_scraper).start()

        time.sleep(10)
        setFlagToStop()
        print("current flag: ", stopScrapperFlag)