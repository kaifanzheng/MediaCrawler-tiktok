from django.test import TestCase
from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .crawlerFunction.DY_liveScraper import get_live_user_name
# Create your tests here.
# class SearchByKeywordTest(TestCase):
#     def test_search_user(self):
#         searchUserByKeyword(3, "servo motor", True)

#     def test_search_video(self):
#         searchVideoByKeyword(3, "servo motor", True)
class LiveScraperTest (TestCase):
    def test_get_live_comment_below_user_name(self):

        queue = get_live_user_name("https://live.douyin.com/498526330292")
        print (list(queue.queue))
        self.assertTrue(queue.qsize()>0)