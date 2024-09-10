from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import RegistrationForm, UserUpdateForm

def userRegister(request):
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
    return render(request, 'post/home.html')

def profile(request, username):
    try:
        targetUser = User.objects.get(username=username)
        context = {'targetUser': targetUser}
        return render(request, 'user/profile.html', context)
    except User.DoesNotExist:
        return render(request, 'post/home.html')

@login_required
def userEdit(request):
    if request.method == 'POST':
        form =UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)        
            
    else: 
            form = UserUpdateForm(instance=request.user)
    return render(request, 'user/edit.html', {'form':form})