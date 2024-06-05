# mediaCrawlerApp/views.py
from django.shortcuts import render
from .crawlerFunction.DY_liveScraper import setFlagToStop, setFlagToStart
from .crawlerFunction.dy_live_scraper import test_get_live_user_name  # 确保正确导入
from django.http import JsonResponse
from .repository import *
from django.views.decorators.csrf import csrf_exempt
import json
import threading

scraperRepo = TikTokUserScraper()

@csrf_exempt
def start_scrapper(request):
    print("后端代码被调用")
    if request.method == 'POST':
        setFlagToStart()
        def run_scraper():
            scraperRepo.scrapeTikTokUsers()  # 使用 scraperRepo 调用

        threading.Thread(target=run_scraper).start()
        return JsonResponse({'status': 'success', 'message': 'Scraper started.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def scrape_users_to_fronted(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url', '')
        print(f"Received URL for scraping: {url}")
        test_get_live_user_name(url)
        return JsonResponse({'status': 'success', 'message': f'Received URL: {url}'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def pulse_scrapper(request):
    if request.method == 'POST':
        setFlagToStop()
        return JsonResponse({'status': 'success', 'message': 'Scraper stopped.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def stop_scrapper(request):
    if request.method == 'POST':
        setFlagToStop()
        scraperRepo.generateSimilarUsers()
        scraperRepo.findMatchTiktokUser()
        results = scraperRepo.getReuslts()
        scraperRepo.emptyData()
        return JsonResponse({'status': 'success', 'message': 'Scraper stopped.', 'data': results})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def set_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url = data.get('url', '')
            scraperRepo.setUrl(url)
            return JsonResponse({'status': 'success', 'message': 'URL set.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
