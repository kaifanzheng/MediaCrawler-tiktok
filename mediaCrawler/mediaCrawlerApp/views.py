from django.shortcuts import render
from .crawlerFunction.DY_liveScraper import setFlagToStop,setFlagToStart
from django.http import JsonResponse
from .repository import *
import json
import threading

scraperRepo = TikTokUserScraper()

def start_scrapper(request):
    if request.method == 'POST':
        setFlagToStart()
        def run_scraper():
            scraperRepo.scrapeTikTokUsers()

        threading.Thread(target=run_scraper).start()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def pulse_scrapper(request):
    if request.method == 'POST':
        setFlagToStop()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def stop_scrapper(request):
    if request.method == 'POST':
        setFlagToStop()
        scraperRepo.generateSimilarUsers()
        scraperRepo.findMatchTiktokUser()
        results = scraperRepo.getReuslts()
        scraperRepo.emptyData()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.', 'data': results})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def set_url(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url= data.get('url', '')
            scraperRepo.setUrl(url)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
# Create your views here.
