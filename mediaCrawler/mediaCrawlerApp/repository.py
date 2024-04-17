from .crawlerFunction.searchByKeyword import searchUserByKeyword, searchVideoByKeyword
from .models import TikTokUser, LiveStreamVideo, SimilarUser
from .crawlerFunction.DY_liveScraper import get_live_user_name
import socket

userdata = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data'


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

def scrapeTikTikUsers():
    tikTokUserQueue = get_live_user_name("https://live.douyin.com/135438115353",userdata)

    while True:
        if tikTokUserQueue.empty():
            break 
        username = tikTokUserQueue.get()
        user = TikTokUser(name=username, ip=get_ip_address())
        user.save()

def generateSimilarUsers():
    #TODO
    all_users = TikTokUser.objects.all()
    for user in all_users:
        username = user.name
        searchResult = searchUserByKeyword(3,username,userdata,True)
        similar_user = SimilarUser(
            tiktok_user = user,
            user_id = searchResult[1],
            name= searchResult[0],
            url="https://example.com",
            ip="192.168.1.2"
        )
        similar_user.save()

    

def findMatchTiktokUser():
    #TODO
    return 0

