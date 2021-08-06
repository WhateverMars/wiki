from random import random
from re import search
from unicodedata import name
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("wiki/<str:entry>", views.entry, name="entry")
    
]
