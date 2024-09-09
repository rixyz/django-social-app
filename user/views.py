from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')        
            
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form':form})

def userLogin(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            context = {'error': 'Invalid username or password'}
    
    return render(request, 'user/login.html', context) 

def home(request):
    return render(request, 'user/home.html')