from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_http_methods, require_POST

from .forms import CustomUserCreationForm, CustomUserChangeForm

import json

from community.models import Review

# Create your views here.
@ require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)



@ require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
@require_POST
def logout(request):
    auth_logout(request)
    return redirect('community:index')


@login_required
def profile(request, user_pk):
    with open('./movies/fixtures/TMDB_movies.json', 'r', encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        movies = json_data

    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)

    reviews = Review.objects.filter(user=request.user)

    reviews_movies = []

    for review in reviews:

        for movie in movies:
            if review.movie_title == movie['title']:
                reviews_movie_title = str(movie['title'])
                reviews_reveiw_title = str(review.title)
                reviews_poster = str(movie['poster_path'])
                reviews_rank = str(review.rank)
                reviews_movies.append(dict(movie_title=reviews_movie_title, review_title=reviews_reveiw_title, poster=reviews_poster, rank=reviews_rank))


    context = {
        'reviews_movies':reviews_movies,
        'person':person,
    }
    # print(reviews_movies)
    return render(request, 'accounts/profile.html', context)


@login_required
@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        you = get_object_or_404(get_user_model(), pk=user_pk)
        me = request.user

        if me != you:
            if you.followers.filter(pk=me.pk).exists():
                you.followers.remove(me)
            else:
                you.followers.add(me)
        return redirect('accounts:profile', you.pk)
    return redirect('accounts:login')



@ login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('community:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)