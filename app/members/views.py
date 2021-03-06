import imghdr
import io
import json
from pprint import pprint

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForms, SignupForms, UserProfileForm

User = get_user_model()

def login_view(request):
    # url : /members/login/
    # config.urls '/members/'부분을 'members.urls include'
    # members.urls 에서 /login/부분을 view 에 연결
    # done

    # template : members/login.html
    # template has username, password form 사용
    # template GET request takes LoginForm
    # nothing for POST

    # form : members/forms.py
    # login form
    # username, password input
    # password widget PasswordInput
    context = {}

    if request.method == 'POST':
        # request.POST gets data
        # username and password put to username and password
        # username/password -> check
        # if authentication success, session/cookie base login / redirect to posts:post-list page
        # if fail, let them know log in failed.
        form = LoginForms(request.POST)
        if form.is_valid():
            login(request, form.user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('posts:post-list')
    else:
        form = LoginForms()

    context['form'] = form
    return render(request, 'members/login.html', context)


def logout_view(request):
    # url = /members/logout
    # no template > redirect to post:post-list
    # base.html 'logout'button takes to this view
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')
    else:
        pass


def signup_view(request):
    # url = /members/signup/
    # template : members/signup.html
    # Form
    #   SignupForm
    #       username, password1, password2
    # rest take login.html attrs

    # GET 요청 시 해당 템플릿 보여주도록 처리
    #  base.html에 있는 signup 버튼이 이 쪽으로 올 수 있도록 url 링크걸기
    form = SignupForms()
    context = {}

    if request.method == 'POST':
        # POST로 전달된 데이터 확인
        # 검증에 성공하면 user생성 redirect to post-list
        # (is_valid()가 true면 올바르다고 가정
        form = SignupForms(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post-list')
    else:
        # GET요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
        # signup.html에 빈 Form또는 올바르지 않은 데이터에 대한 정보가 포함된 Form 을 전달해서 동적으로 form 을 렌더링
        form = SignupForms()
    context['form'] = form
    return render(request, 'members/signup.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # 수정이 완료되면 message모듈을 사용해서 템플릿에 수정완료 메시지를 표시(숙제)
            messages.success(request,'Profile update succeeded')
    form = UserProfileForm(instance=request.user)
    context={
        'form':form
    }
    return render(request, 'members/profile.html', context)

def facebook_login(request):
    user=authenticate(request,facebook_request_token=request.GET.get('code'))
    if user:
        login(request, user)
        return redirect('posts:post-list')
    messages.error(request, 'facebook login failed')
    return redirect('members:login-view')