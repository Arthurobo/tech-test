from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from account.forms import (RegistrationForm, AccountAuthenticationForm, 
                            AccountUpdateForm, ProfileImageUpdateForm, UserProfileUpdateForm)
from django.conf import settings
from account.models import Account, Profile
from django.forms.models import model_to_dict
from django.views.generic import View, CreateView, DetailView, ListView
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import os
import cv2
import json
import base64
import io, csv
from django.core import files

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"


def register_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect("public:home")

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            sex = form.cleaned_data.get('sex')
            status = form.cleaned_data.get('status')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password,
                                    first_name=first_name, last_name=last_name, sex=sex, status=status)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("public:home")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('public:home')


# New login view that redirects and not like the old login 
# view that uses the get_redirect_f _exists
def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("public:home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if request.GET:
                    if request.GET.get("next"):
                        return redirect(request.GET.get('next'))
                return redirect("public:home")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
    # redirect = None
    redirect = settings.LOGIN_REDIRECT_URL
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("NEXT"))
    return redirect


@login_required
def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    #page = Page.objects.filter(owner=request.user.profile)#.order_by('-cr_date')
    try:
        account = Account.objects.get(pk=user_id)
        profile = Profile.objects.get(pk=user_id)
        # page = Page.objects.filter(owner=profile.user_id).order_by('-date_created')
        # post = Post.objects.filter(author=profile.user_id)
    except:
        return HttpResponse('Something went wrong.')

    if request.method == "GET":
        context['id'] = account.id
        context['subjects_taught'] = account.subjects_taught
        context['phone_number'] = account.phone_number
        context['first_name'] = account.first_name
        context['last_name'] = account.last_name
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
        context['room_number'] = account.room_number

        is_self = True
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False

        elif not user.is_authenticated:
            is_self = False
    
            # Set the template variables to the values
        context['is_self'] = is_self
        # context['BASE_URL'] = settings.BASE_URL
    


        return render(request, "account/account.html", context)

    
@login_required
def edit_account_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = kwargs.get("user_id")
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}
    if request.POST:
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                    initial={
                        "id": account.pk,
                        "email": account.email,
                        "first_name": account.first_name,
                        "last_name": account.last_name,
                        "hide_email": account.hide_email,
                        "phone_number": account.phone_number,
                    })
            context['form'] = form
    else:
        form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email,
					"first_name": account.first_name,
					"last_name": account.last_name,
					"hide_email": account.hide_email,
					"phone_number": account.phone_number,
				}
			)
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'account/edit_account.html', context)



@login_required
def edit_user_profile_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    profile = Profile.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile credentials.")
    
    context = {}
    if request.POST:
        form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = UserProfileUpdateForm(request.POST, instance=request.user.profile,
                initial = {
                    "id": profile.pk,
                    "room_number": profile.room_number,
                })
            context['form'] = form
    else:
        form = UserProfileUpdateForm(
            initial={
                    "id": profile.pk,
                    "room_number": profile.room_number,
                }
            )
        context['form'] = form
    return render(request, "account/edit_profile.html", context)


@login_required
def edit_profile_image_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('account:login')
    user_id = kwargs.get('user_id')
    account = Account.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile Image.")
    context = {}
    if request.POST:
        form = ProfileImageUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect("account:user-account-view", user_id=account.pk)
        else:
            form = ProfileImageUpdateForm(request.POST, instance=request.user,
                initial = {
                    "id": account.pk,
                    "profile_image": account.profile_image,
                })
            context['form'] = form
    else:
        form = ProfileImageUpdateForm(
            initial={
                "id": account.pk,
                "profile_image": account.profile_image,
                }
            )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "account/edit_profile_image.html", context)
