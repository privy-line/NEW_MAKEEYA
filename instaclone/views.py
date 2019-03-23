from django.shortcuts import render
from django.http  import HttpResponse,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
 
 
 
@login_required(login_url='/accounts/login/')
def home(request): 
    title = 'Home' 
    return render(request, 'home.html', {'title':title,})

 