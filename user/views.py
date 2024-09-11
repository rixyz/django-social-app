from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import RegistrationForm, UserUpdateForm

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')        
            
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form':form})

def user_login(request):
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

def profile(request, username):
    try:
        targetUser = User.objects.get(username=username)
        context = {'targetUser': targetUser}
        return render(request, 'user/profile.html', context)
    except User.DoesNotExist:
        return render(request, 'post/home.html')

@login_required
def user_edit(request):
    if request.method == 'POST':
        print("YES")
        form =UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            for file_name, file_obj in request.FILES.items():
                print(file_name, file_obj) 
            form.save()
            return redirect('profile', request.user.username)        
            
    else: 
            form = UserUpdateForm(instance=request.user)
    return render(request, 'user/edit.html', {'form':form})