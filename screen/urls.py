from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"), # url to add info about cinema
    path('<slug:screen>/reserve/', views.reserve, name="reserve"), # url to reserve tickets with slug as variable to screen name
    path('<slug:screen>/seats', views.available, name="available") # url used both for finding suitable seats and available vacant seats
]
