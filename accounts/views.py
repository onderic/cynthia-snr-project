from django.shortcuts import render, redirect
from .forms import signUpForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = signUpForm()
    return render(request, 'authentication/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the next page if it exists, otherwise redirect to a default page
            next_page = request.GET.get('next', '/') 
            return redirect(next_page)
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid credentials'})
    return render(request, 'authentication/login.html')

