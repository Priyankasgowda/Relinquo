from django.contrib import admin
from webserver.views import *
from django.urls import path,include

urlpatterns = [
    path('',homepage),
    path('getstarted/',signup),
    path('team/', team),
    path('login/',signin),
    path('dashboard/',dashboard),
    path('team/',team),
    path('employee/',employee)
]
