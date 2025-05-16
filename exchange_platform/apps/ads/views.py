from django.shortcuts import render
from uuid import uuid4
from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout



from .forms import *
from .models import *


def index(request):
	# form = LoginForm()
	# if request.method == 'POST':
	# 	form = LoginForm(request.POST)
	# 	if form.is_valid():
	# 		print(form.cleaned_data)
	# return render(request, 'showdb/auth.html', {"form": form})
	return render(request, 'ads/index.html')

def auth(request):
	return render(request, 'ads/auth.html')


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
		orgs = Clients.objects.all()
		return HttpResponseRedirect( reverse('showdb:orgs'))
		# return render(request, 'showdb/orgs.html', {'orgs': orgs})
	else:
		return HttpResponseRedirect( reverse('showdb:index'))
		# return render(request, 'showdb/auth.html')

def log_out(request):
	logout(request)
	return HttpResponseRedirect( reverse('showdb:index'))
	# return render(request, 'showdb/auth.html')

