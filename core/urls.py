from django.urls import path

from .views import RegisterUser
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    
    path('register', RegisterUser.as_view(), name = 'register'),
    path('signin', views.signin, name = 'signin'),

    path('markSpam', views.markSpam, name = 'markSpam'),

    path('search/name', views.searchName, name = 'searchName'),
    path('search/phone', views.searchPhone, name = 'searchPhone'),

    path('search/detail', views.searchDetail, name = 'searchDetail'),

    ####################################################
]
