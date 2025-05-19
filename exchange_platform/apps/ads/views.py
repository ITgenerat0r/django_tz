from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, FileResponse
from django.urls import reverse

from uuid import uuid4
from datetime import datetime, timedelta
import json
from django.contrib.auth import authenticate, login, logout



from .forms import *
from .models import *

def get_current_time(step=0):
        # return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return (datetime.now() + timedelta(seconds=step)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def index(request):
	print(f"User: {request.user}")
	if not request.user.is_authenticated:
		return auth(request)
	return render(request, 'ads/index.html')

def auth(request):
	return render(request, 'ads/auth.html')

	if not request.user.is_authenticated:
		form = LoginForm()
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				print(form.cleaned_data)
		return render(request, 'ads/auth.html', {"form": form})
	return HttpResponseRedirect( reverse('ads:index'))



def check_user_access_to_group(request, target_group="editor"):
	if not request.user.is_authenticated:
		return False
	groups = request.user.groups.all()
	for group in groups:
		if str(group) == target_group:
			return True
	return False



def log_in(request):
	print("Request:")
	username = request.POST["login"]
	password = request.POST["password"]
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponseRedirect( reverse('ads:main'))
	else:
		return HttpResponseRedirect( reverse('ads:auth'))

def log_out(request):
	logout(request)
	return HttpResponseRedirect( reverse('ads:auth'))




def my_ads(request):
	if not request.user.is_authenticated:
		return auth(request)
	ads = Ad.objects.filter(user=request.user)
	return render(request, 'ads/main.html', {'ads': ads})



def all_ads(request):
	if not request.user.is_authenticated:
		return auth(request)
	ads = Ad.objects.all()
	return render(request, 'ads/main.html', {'ads': ads})



def ad_view(request, ad_id):
	print(f"ad_view({ad_id})")
	ad = Ad.objects.get(id=ad_id)
	is_owner = ad.user == request.user
	return render(request, 'ads/ad.html', {'ad': ad, 'is_owner': is_owner})


def new_ad(request):
	if not request.user.is_authenticated:
		return auth(request)
	form = AdForm()
	if request.method == 'POST':
		form = AdForm(request.POST)
		if form.is_valid():
			ad = form.save(commit=False)
			ad.user = request.user
			ad.created_at = get_current_time()[:10]
			ad.save()
			return ad_view(request, ad.id)
	text = ''
	return render(request, 'ads/new_ad.html', {'form': form})


def edit_ad(request, ad_id):
	if not request.user.is_authenticated:
		return auth(request)
	ad = Ad.objects.get(id=ad_id)
	if ad.user == request.user:
		if request.method == 'POST':
			form = AdForm(request.POST)
			if form.is_valid():
				ad.save()
				return ad_view(request, ad.id)
		form = AdForm()
		if ad:
			form.set_ad(ad)
		return render(request, 'ads/edit_ad.html', {'form': form, 'ad_id': ad.id})
	else:
		return render(request, 'ads/my_ads')

def update_ad(request, ad_id):
	if not request.user.is_authenticated:
		return auth(request)
	form = AdForm()
	if request.method == 'POST':
		form = AdForm(request.POST)
		if form.is_valid():
			ad = Ad.objects.get(id=ad_id)
			if ad and ad.user == request.user:
				if form.cleaned_data['title']:
					ad.title = form.cleaned_data['title']
				if form.cleaned_data['description']:
					ad.description = form.cleaned_data['description']
				if form.cleaned_data['image_url']:
					ad.image_url = form.cleaned_data['image_url']
				if form.cleaned_data['category']:
					ad.category = form.cleaned_data['category']
				if form.cleaned_data['condition']:
					ad.condition = form.cleaned_data['condition']
				ad.save()
	return edit_ad(request, ad_id)

def delete_ad(request, ad_id):
	if not request.user.is_authenticated:
		return auth(request)
	ad = Ad.objects.get(id=ad_id)
	if ad.user == request.user:
		Ad.objects.get(id=ad_id).delete()
	return my_ads(request)

