from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods, require_POST

import json
import requests

from community.models import Review


# Create your views here.
def movies_list(request):
    with open('./movies/fixtures/TMDB_movies.json', 'r', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        movies = json_data

    for movie in movies:
        reviews = Review.objects.filter(movie_title=movie['title'])
        review_rank = 0
        for review in reviews:
            review_rank += review.rank
        rank_avg = round(review_rank / len(reviews), 1) if len(reviews) else 0
        movie['rank_avg'] = rank_avg
        movie['total_review'] = len(reviews)

    context = {
        'movies': movies,
    }
    return render(request, 'movies/movies_list.html', context)


def test(request, title):
    with open('./movies/fixtures/TMDB_movies.json', 'r', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        movies = json_data
    
    for movie in movies:
        reviews = Review.objects.filter(movie_title=movie['title'])
        review_rank = 0
        for review in reviews:
            review_rank += review.rank
        rank_avg = round(review_rank / len(reviews), 1) if len(reviews) else 0
        movie['rank_avg'] = rank_avg
        movie['total_review'] = len(reviews)
    
    context = {
        'movies': movies,
        'title': title,
    }
    return render(request, 'movies/test.html', context)


def detail(request, title):
    with open('./movies/fixtures/TMDB_movies.json', 'r', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        movies = json_data


    # 디테일 페이지 렌더링 대상이 되는 영화 검색
    for movie in movies:
        if movie['title'] == title:
            target_movie = movie
            break
    
    # 영화 장르 결정
    genres = {
        28: '액션',
        12: '모험',
        16: '애니메이션',
        35: '코미디',
        80: '범죄',
        99: '다큐멘터리',
        18: '드라마',
        10751: '가족',
        14: '판타지',
        36: '사극',
        27: '공포',
        10402: '음악',
        9648: '미스터리',
        10749: '로맨스',
        878: 'SF',
        10770: 'TV영화',
        53: '스릴러',
        10752: '전쟁',
        37: '서부극',
    }
    if movie['genre_ids']:
        genre = genres[movie['genre_ids'][0]]
    else:
        genre = genres[53]
        
    # 해당 영화 리뷰를 검색하여 평점을 계산
    reviews = Review.objects.filter(movie_title=movie['title'])
    review_rank = 0
    for review in reviews:
        review_rank += review.rank
    
    rank_avg = round(review_rank / len(reviews), 1) if len(reviews) else 0

    target_movie['rank_avg'] = rank_avg

    # youtube api로 요청을 보내서 영화 trailer를 가져옴
    API_KEY = 'AIzaSyD6Bby3u4Uz2rbTOdQPzpwyTRDemRYUD5k'
    API_URL = 'https://www.googleapis.com/youtube/v3/search'

    params = {
        'key': API_KEY,
        'part': 'snippet',
        'type': 'video',
        'q': title + 'trailer',
    }
    r = requests.get(API_URL, params)
    trailer = 'https://www.youtube.com/embed/' + r.json()['items'][0]['id']['videoId']
    link = 'https://www.youtube.com/watch?v=' + r.json()['items'][0]['id']['videoId']

    context = {
        'movie': target_movie,
        'reviews': reviews,
        'genre': genre,
        'trailer': trailer,
        'link': link,
    }
    return render(request, 'movies/detail.html', context)