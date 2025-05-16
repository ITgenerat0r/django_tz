from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, FileResponse
from django.urls import reverse

from uuid import uuid4
from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout



from .forms import *
from .models import *


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
	# # data = Botool.objects.all()[:10]
	# # data = {'one', 'two', 'three'}
	# titles = Titles.objects.all()
	# # devices = Devices.objects.all()
	# # orgs = Clients.objects.all()
	# return render(request, 'tseditor/titles.html', {'titles': titles, 'techsupport': 'techsupport'})


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
		# orgs = Clients.objects.all()
		return HttpResponseRedirect( reverse('ads:index'))
		# return render(request, 'showdb/orgs.html', {'orgs': orgs})
	else:
		return HttpResponseRedirect( reverse('ads:auth'))
		# return render(request, 'showdb/auth.html')

def log_out(request):
	logout(request)
	return HttpResponseRedirect( reverse('ads:auth'))
	# return render(request, 'showdb/auth.html')

