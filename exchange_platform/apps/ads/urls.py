from django.urls import path
from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.auth, name = 'auth'),
path('log_in', views.log_in, name = 'log_in'),
path('logout', views.log_out, name = 'logout'),

path('index', views.index, name='index'),

]
