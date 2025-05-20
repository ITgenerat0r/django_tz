from django.urls import path
from . import views

app_name = 'showdb'
urlpatterns = [
path('', views.auth, name = 'auth'),
path('log_in', views.log_in, name = 'log_in'),
path('logout', views.log_out, name = 'logout'),
path('main', views.all_ads, name = 'main'),
path('my_ads', views.my_ads, name = 'my_ads'),
path('ad/<int:ad_id>', views.ad_view, name = 'ad'),
path('new_ad', views.new_ad, name = 'new_ad'),
path('edit_ad/<int:ad_id>', views.edit_ad, name = 'edit_ad'),
path('update_ad/<int:ad_id>', views.update_ad, name = 'update_ad'),
path('delete_ad/<int:ad_id>', views.delete_ad, name = 'delete_ad'),
path('new_comment/<int:ad_id>', views.new_comment, name = 'new_comment'),
path('delete_comment/<int:proposal_id>', views.delete_comment, name = 'delete_comment'),
path('proposal_response/<int:proposal_id>/<int:res>', views.proposal_response, name = 'proposal_response'),
# path('create_ad', views.create_ad, name = 'create_ad'),

path('index', views.index, name='index'),

]
