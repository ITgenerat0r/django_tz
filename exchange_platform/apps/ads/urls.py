from django.urls import path
from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.index, name = 'index'),

]
