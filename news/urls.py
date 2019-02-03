from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('articles/', views.index, name='index'),
    path('articles/detail/<int:id>/',views.PostDetail, name='PostDetail'),
    path('articles/post-all/',views.AllPost, name='AllPost'),
    path('articles/category/<name>',views.PostCategory, name='category'),
    path('articles/author-profile/<name>',views.getAuthor,name='author'),
    path('articles/profile', views.CreateProfile, name='profile'),
    path('articles/signup', views.signup, name='signup'),
    path('articles/login/',views.LogIn, name='login'),
    path('articles/logout/',views.LogOut, name='logout'),
    path('articles/post-create/', views.post_create, name='post_create'),
    path('articles/post_update/<int:id>', views.PostUpdate, name='post_update'),
    path('articles/post_update/<int:id>', views.PostDelete, name='post_delete'),

]