from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.http import HttpResponseNotAllowed

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account registered successfully. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'users/logout.html')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def profile(request):
    return render(request, 'users/profile.html')