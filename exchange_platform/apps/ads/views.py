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
	# return render(request, 'ads/auth.html')

	if not request.user.is_authenticated:
		form = LoginForm()
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				print(form.cleaned_data)
		return render(request, 'ads/auth.html', {"form": form})
	return HttpResponseRedirect( reverse('ads:main'))



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
	ads = Ad.objects.exclude(user=request.user)
	return render(request, 'ads/main.html', {'ads': ads})



def ad_view(request, ad_id):
	print(f"ad_view({ad_id})")
	ad = Ad.objects.get(id=ad_id)
	proposals = ExchangeProposal.objects.filter(ad_sender=ad)
	comment_form = CommentForm(request.user)
	return render(request, 'ads/ad.html', {
		'ad': ad, 
		'is_owner': ad.user == request.user,
		'user': request.user, 
		'proposals': proposals, 
		'comment_form':comment_form})


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


def new_comment(request, ad_id):
	if not request.user.is_authenticated:
		return auth(request)
	ad = Ad.objects.get(id=ad_id)
	if request.method == 'POST':
		form = CommentForm(request.user, request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			proposal = form.save(commit=False)
			proposal.ad_sender = ad
			proposal.status = "Ожидает"
			proposal.created_at = get_current_time()[:10]
			proposal.save()
			print("SAVE")
			return ad_view(request, ad.id)
		else:
			print("NOT VALID")
			print(form.errors)
	return ad_view(request, ad.id)

def delete_comment(request, proposal_id):
	if not request.user.is_authenticated:
		return auth(request)
	proposal = ExchangeProposal.objects.get(id=proposal_id)
	ad_id = proposal.ad_sender.id
	if proposal.ad_receiver.user == request.user:
		proposal.delete()
	return ad_view(request, ad_id)


def proposal_response(request, proposal_id, res):
	if not request.user.is_authenticated:
		return auth(request)
	proposal = ExchangeProposal.objects.get(id=proposal_id)
	ad_id = proposal.ad_sender.id
	if proposal.ad_sender.user == request.user:
		if res:
			ad_sender = Ad.objects.get(id=proposal.ad_sender.id)
			ad_receiver = Ad.objects.get(id=proposal.ad_receiver.id)
			if not ad_sender.is_bonded and not ad_receiver.is_bonded:
				ad_sender.is_bonded = True
				ad_receiver.is_bonded = True
				proposal.status = "Принят"
				ad_sender.save()
				ad_receiver.save()
				proposals = ExchangeProposal.objects.filter(ad_receiver=ad_receiver, status="Ожидает")
				proposals.delete()
		else:
			proposal.status = "Отклонен"
		proposal.save()
	return ad_view(request, ad_id)

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

