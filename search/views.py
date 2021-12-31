import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect
from random import randrange
import random

def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        year = 2020
        keyWord = ""
        if(request.POST['search_year']):
            year = request.POST['search_year']
        else:
            year = random.randint(1920, 2020)

        if(request.POST['search_type']):
            keyWord = request.POST['search_type']
        else:
            temp = random.randint(0, 13)
            listOfWords = ['Rock','Metal','Latin','R&B','Soul','Flok','Blues','World','Classical','Jazz','New age','Pop','Country','Mariachi']
            keyWord = listOfWords[temp]
        searchValue = keyWord+" music "+str(year)
        search_params = {
            'part' : 'snippet',
            'q' : searchValue,
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        rNumber = randrange(len(results))
        video_data = {
            'title' : results[rNumber]['snippet']['title'],
            'id' : results[rNumber]['id'],
            'url' : f'https://www.youtube.com/watch?v={ results[rNumber]["id"] }',
            'duration' : int(parse_duration(results[rNumber]['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail' : results[rNumber]['snippet']['thumbnails']['high']['url']
        }

        videos.append(video_data)

    context = {
        'videos' : videos
    }
    
    return render(request, 'search/index.html', context)
