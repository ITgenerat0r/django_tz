from django.shortcuts import render
from uuid import uuid4
from datetime import datetime
import json



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

