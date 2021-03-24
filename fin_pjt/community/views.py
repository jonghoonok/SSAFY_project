from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

from .models import Review, Comment
from .forms import ReviewForm, CommentForm

import json

# Create your views here.
def home(request):
    return render(request, 'community/home.html')

def index(request): # 홈 개념
    with open('./movies/fixtures/TMDB_movies.json', 'r', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        movies = json_data

    popularity_lists = sorted(movies, key=lambda x: round(x['vote_average']), reverse=True)
    popularitys = []
    posters = []
            
    cnt = 0
    for popularity_list in popularity_lists:
        cnt += 1
        poster_lst = str(popularity_list['poster_path'])
        poster_title = str(popularity_list['title'])
        poster_vote_average = str(popularity_list['vote_average'])
        poster_id = cnt
        poster_release_date = str(popularity_list['release_date'])
        poster_overview = str(popularity_list['overview'])
        popularitys.append(dict(poster=poster_lst, title=poster_title, vote_average=poster_vote_average, id=poster_id, release_date=poster_release_date, overview=poster_overview))
        if cnt == 10:
            break

    if request.user.is_authenticated:
        
        review_movie_titles = Review.objects.filter(user_id = request.user.pk).values('movie_title')

        if len(review_movie_titles) != 0:
            reviewd_movies = []

            for review_movie_title in review_movie_titles:
                lst = str(review_movie_title['movie_title'])
                reviewd_movies.append(lst)
            
            my_genres = []

            for reviewd_movie in reviewd_movies:
                for movie in movies:
                    if movie['title'] == reviewd_movie:
                        for q in movie['genre_ids']:
                            my_genres.append(q)

            genre_cnt = 0
            my_favorite_genre = ''

            for my_genre in my_genres:
                if my_genres.count(my_genre) > genre_cnt:
                    genre_cnt = my_genres.count(my_genre)
                    my_favorite_genre = my_genre

            cnt = 0

            for popularity_list in popularity_lists:
                if cnt == 10:
                    break
                if my_favorite_genre in popularity_list['genre_ids']:
                    if popularity_list['title'] not in reviewd_movies:
                        cnt += 1
                        poster_lst = str(popularity_list['poster_path'])
                        poster_title = str(popularity_list['title'])
                        poster_vote_average = str(popularity_list['vote_average'])
                        poster_id = cnt
                        poster_release_date = str(popularity_list['release_date'])
                        poster_overview = str(popularity_list['overview'])
                        posters.append(dict(poster=poster_lst, title=poster_title, vote_average=poster_vote_average, id=poster_id, release_date=poster_release_date, overview=poster_overview))
                        if cnt == 10:
                            break
   

    context = {
        'posters':posters,
        'popularitys':popularitys,
    }

    return render(request, 'community/index.html', context)


@require_http_methods(['GET','POST'])
def create(request, movie_name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(initial={
                'movie_title': movie_name
            })
        context ={
            'form':form,
            'movie_title': movie_name,
        }
        return render(request, 'community/form.html', context)
    return redirect('community:index')


def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    star = review.rank
    cnt = 0
    stars=[]
    for i in range(star//2):
        stars.append(2)
        cnt += 1
    if star % 2:
        stars.append(1)
        cnt += 1
    while cnt < 5:
        stars.append(0)
        cnt +=1

    comment_form = CommentForm()
    comments = review.comment_set.all()
    context ={
        'review':review,
        'comment_form':comment_form,
        'comments':comments,
        'stars':stars,
        'user':False
    }
    if request.user == review.user:
        context['user'] = True

    return render(request, 'community/detail.html', context)


@require_POST
def delete(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('community:detail', review.pk)


@require_POST
def create_comment(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('community:detail', review.pk)
        context ={
            'comment_form':comment_form,
            'review':review,
        }
        return render(request, 'community/detail.html', context)
    return redirect('accounts:login')


@require_POST
def delete_comment(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('community:detail', review.pk)



def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)
        return redirect('community:detail', review.pk)
    return redirect('accounts:login')



@require_http_methods(['GET','POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance = review)
        if form.is_valid():
            form.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm(instance = review)
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)