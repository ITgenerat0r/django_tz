from django.urls import path
from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.auth, name = 'auth'),
path('log_in', views.log_in, name = 'log_in'),
path('logout', views.log_out, name = 'logout'),
path('main', views.all_ads, name = 'main'),
path('my_ads', views.my_ads, name = 'my_ads'),
path('ad/<ad_id>', views.ad_view, name = 'ad'),
path('new_ad', views.new_ad, name = 'new_ad'),
path('create_ad', views.create_ad, name = 'create_ad'),

path('index', views.index, name='index'),

]
