# mediaCrawlerApp/urls.py
from django.urls import path
from mediaCrawlerApp.utils.recall_data import download_excel
from mediaCrawlerApp.utils.random_text import random_text_view
from .views import start_scrapper, pulse_scrapper, stop_scrapper, set_url, scrape_users_to_fronted

urlpatterns = [
    path('random-text/', random_text_view, name='random_text'),
    path('test-scrape-users/', scrape_users_to_fronted, name='test_scrape_users'),
    path('start-scraper/', start_scrapper, name='start_scraper'),
    path('pause/', pulse_scrapper, name='pause_scrapper'),
    path('download-excel/', download_excel, name='download_excel'),
]
