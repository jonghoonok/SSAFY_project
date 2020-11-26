from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('list/', views.movies_list, name="movies_list"),
    path('test/<str:title>', views.test, name="test"),
    path('detail/<str:title>', views.detail, name="detail"),
]
