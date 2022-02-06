import imp
from django.shortcuts import render

from .views_extend.scrape_artnews import *
from .views_extend.scrape_bigThink import *

# Create your views here.
def index (request):

    # Scrape Artnews; funcition from: .views_extend.scrape_artnews
    news = scrape_artnews_funct()

    return render (request, 'scraper/index.html', {
        'news': news,
    })

def think (request):

    bigThink = scrape_bigThink_funct()

    return render (request, 'scraper/think.html', {
        'bigThink': bigThink,
    })