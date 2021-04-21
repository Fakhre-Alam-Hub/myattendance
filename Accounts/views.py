from django.shortcuts import render, redirect
from Accounts.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Accounts.models import Profile
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to login!')
            return redirect('account_login')
    else:
        form = UserRegisterForm()

    return render(request, 'Accounts/register.html', {'form':form})  


# login is required to access this route
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, template_name='Accounts/profile.html', context=context)
