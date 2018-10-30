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
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token?'
    api_me = f'{api_base}/me'
    code = request.GET.get('code')
    #request token to access token using 'requests'

    #VERY IMPORTANT. NO HARDCODING
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code':code
    }

    response = requests.get(api_get_access_token,params)
    # response_object = json.loads(response.text)
    # # return HttpResponse('{}, {}'.format(response_object, type(response_object)))

    data = response.json()
    access_token = data['access_token']

    # using access token to bring user info

    params = {
        'access_token' : access_token,
        'fields':', '.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ]),
    }
    response = requests.get(api_me,params)
    data = response.json()
    pprint(data)

    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']
    # requesting for image url
    img_response = requests.get(url_img_profile)
    img_data = img_response.content
    # extension finder from binary
    ext = imghdr.what('',h=img_data)
    # first parameter for name, and second for binary file
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)
    try:
        user = User.objects.get(username=facebook_id)
        user.last_name = last_name
        user.first_name = first_name
        # user.img_profile = f
        user.save()

    except User.DoesNotExist:
        user = User.objects.create_user(
        username=facebook_id,
        first_name=first_name,
        last_name=last_name,
        img_profile=f,)

    login(request, user)
    return redirect('posts:post-list')