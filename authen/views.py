from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from base.models import CartModel
from django.contrib.auth.decorators import login_required
from .models import ProfilePic


# Create your views here.
def login_(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['pasw']
        user = authenticate(username = uname, password = password)
        if user:
            login(request,user)
            messages.success(request,'Login Successful')
            return redirect('home')
        else:
            messages.error(request,'Username or Password is Incorrect')
            return redirect('login')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        try:
            User.objects.get(username = request.POST['uname'])
            messages.error(request,'Username already exists..!')
            return redirect('register')
        except:
            user = User.objects.create_user(
                first_name = request.POST['fname'],
                last_name = request.POST['lname'],
                email = request.POST['email'],
                username = request.POST['uname'],
                password = request.POST['pasw'],
            )

            ProfilePic.objects.create(
                host = user,
                pimage = request.FILES.get('pimage')
            )
            
            messages.success(request,'New User Registered Successfully..!')
            return redirect('register')
    return render(request,'register.html')

@login_required
def profile(request):
    cart_count = CartModel.objects.filter(host=request.user).count()
    profile, created = ProfilePic.objects.get_or_create(
        host=request.user,
        defaults={'pimage': 'default_profile.webp'}
    )
    return render(request,'profile.html',{'cart_count': cart_count, 'profile': profile})

@login_required
def logout_(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('profile')

@login_required
def update(request):
    cart_count = CartModel.objects.filter(host = request.user).count()
    user = User.objects.get(username = request.user)
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        username = request.POST['uname']
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        return redirect('profile')
    return render(request,'update.html',{'data':user,'cart_count':cart_count})

@login_required
def reset(request):
    cart_count = CartModel.objects.filter(host = request.user).count()
    if request.method == 'POST':
        if 'old_pasw' in request.POST:
            print(request.POST)
            old_pasw = request.POST['old_pasw']
            user = authenticate(username = request.user, password = old_pasw)
            if user:
                return render(request,'reset.html',{'new':True})
            else:
                messages.error(request,'Entered old password is wrong')
                return redirect('reset')
            
        if 'new_pasw' in request.POST:
            print(request.POST)
            new_pasw = request.POST['new_pasw']
            user = User.objects.get(username = request.user)
            user.set_password(new_pasw)
            user.save()
            messages.success(request,'Password updated successfully')
            return redirect('login')

    return render(request,'reset.html',{'cart_count':cart_count})

def fpass(request):
    if request.method =='POST':
        if 'uname' in request.POST:
            username = request.POST['uname']
            try:
                user = User.objects.get(username = username)
                request.session['fpuser'] = user.username
                return render(request,'fpass.html',{'new':True})
            except:
                return render(request,'fpass.html',{'error':True})
            
        if 'password' in request.POST:
            username = request.session.get('fpuser')
            user = User.objects.get(username = username)
            new_pasw = request.POST['password']
            user.set_password(new_pasw)
            user.save()
    return render(request,'fpass.html')