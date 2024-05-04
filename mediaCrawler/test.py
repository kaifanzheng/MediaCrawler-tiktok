from .models import TikTokUser
user_exists = TikTokUser.objects.filter(id=2).exists()
print(user_exists)  # 这应该输出 True