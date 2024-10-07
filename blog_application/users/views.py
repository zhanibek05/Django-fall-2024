from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm, UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from .models import Profile, Follow


# Register view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])  # Set password
            new_user.save()  # Save the user
            profile = Profile.objects.create(user = new_user, bio = "", avatar = None)
            profile.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
        
    template = loader.get_template('register.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

# Login view
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)  # Pass request to the form
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            login(request, user) 
            return redirect('/posts/')  # Redirect to home or another page after login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('/login/')


def user_profile_edit(request):
    profile = request.user.profile  # Get the current user's profile
    followers_count = Follow.objects.filter(following=request.user).count()
    follower_users = Follow.objects.filter(following=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to the same page after saving
    else:
        form = ProfileUpdateForm(instance=profile)  # Pre-populate form with current profile data

    context = {
        'form': form,
        'profile': profile,
        'followers_count': followers_count,
        'follower_users': follower_users,
    }
    return render(request, 'profile.html', context)


def user_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    #check that current user followed or not for this profile
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    #get all followers fo this profile
    followers_count = Follow.objects.filter(following=user).count()
    follower_users = Follow.objects.filter(following=user)
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "follow" and not is_following:
            Follow.objects.create(follower=request.user, following=user)
        
        elif action == "unfollow" and is_following:
            Follow.objects.filter(follower=request.user, following=user).delete()


        return redirect(f'/users/{id}')
    
    
    context = {
        "profile": profile,
        "is_following": is_following,
        "followers_count": followers_count,
        "follower_users": follower_users,
    }
    return render(request, 'follow.html' , context)