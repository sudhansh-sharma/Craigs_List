from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_URL = "https://chandigarh.craigslist.org/search/hhh?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_URL.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text
    # print(data)
    soup = BeautifulSoup(data,'html.parser')

    post_listings = soup.find_all('li', {'class':'result-row'})
    # print(len(post_listings))
    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'No Price Associated With it.'

        image_url = ''

        if post.find(class_="result-image").get('data-ids'):
            image_id = post.find(class_="result-image").get('data-ids').split(',')[0].split(':')[1]
            image_url = BASE_IMAGE_URL.format(image_id)
        else:
            image_url = 'https://us.123rf.com/450wm/ukususha/ukususha1506/ukususha150600009/41983265-stock-vector-vector-peace-symbol-in-watercolor-splashes.jpg?ver=6'

        final_postings.append((post_title, post_url, post_price, image_url))

    # print(len(final_postings))

    stuff_for_frontend = {
        "search":search,
        'final_postings':final_postings,

    }
    return render(request, 'myapp/new_search.html', context=stuff_for_frontend)