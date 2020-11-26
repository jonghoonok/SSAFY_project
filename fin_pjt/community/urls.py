from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.home, name="home"),
    path('community/', views.index, name="index"),
    path('community/<str:movie_name>/create', views.create, name='create'),
    path('community/<int:review_pk>/',views.detail, name='detail'),
    path('community/<int:review_pk>/delete/',views.delete, name='delete'),
    path('community/<int:review_pk>/update/',views.update, name='update'),
    path('community/<int:review_pk>/comments/',views.create_comment, name='create_comment'),
    path('community/<int:review_pk>/comments/<int:comment_pk>/delete/',views.delete_comment, name='delete_comment'),
    path('community/<int:review_pk>/like/',views.like, name='like'),
]
