from django.shortcuts import render
from .crawlerFunction.DY_liveScraper import setFlagToStop
from django.http import JsonResponse
from .repository import scrapeTikTokUsers, generateSimilarUsers,findMatchTiktokUser,emptyData,getReuslts

def start_scrapper(request):
    if request.method == 'POST':
        scrapeTikTokUsers()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def pulse_scrapper(request):
    if request.method == 'POST':
        setFlagToStop()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

def stop_scrapper(request):
    if request.method == 'POST':
        generateSimilarUsers()
        findMatchTiktokUser()

        results = getReuslts()
        emptyData()
        return JsonResponse({'status': 'success', 'message': 'Scrapper stopped.', 'data': results})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# Create your views here.
