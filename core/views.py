from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('level_select')  # change to your dashboard view
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')

    return render(request, 'core/signup.html')

def home(request):
    return render(request, 'core/dashboard.html')



@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or your desired redirect
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def home_redirect(request):
    return redirect('login') 



def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Register logic...
    return render(request, 'core/signup.html')





class CustomSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


