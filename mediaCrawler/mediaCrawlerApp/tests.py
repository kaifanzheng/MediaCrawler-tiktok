from django.test import TestCase
from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword

# Create your tests here.
class SearchByKeywordTest(TestCase):
    def test_search_user(self):
        searchUserByKeyword(3, "servo motor", True)

    def test_search_video(self):
        searchVideoByKeyword(3, "servo motor", True)
