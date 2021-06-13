#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from . import views


app_name = 'note'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<str:word>/<int:days>/', views.query, name='query'),
    path('post/ajax/favorite/<str:word>', views.favorite, name='unfavorite'),
]
