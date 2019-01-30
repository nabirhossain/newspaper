from django.urls import path

from . import views

app_name = 'newsletters'

urlpatterns = [
    path('articles/subscribe/', views.newsletter_subscribe, name='subscribe'),
    path('articles/unsubscribe/',views.newsletter_unsubscribe, name='unsubscribe'),


]