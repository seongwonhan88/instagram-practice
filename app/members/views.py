from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForms, SignupForms


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
    if request.method == 'POST':
        # request.POST gets data
        # username and password put to username and password
        # username/password -> check
        # if authentication success, session/cookie base login / redirect to posts:post-list page
        # if fail, let them know log in failed.
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:  # auth success
            login(request, user)
            return redirect('posts:post-list')
        else:  # auth fail
            pass

    else:
        form = LoginForms()
        context = {
            'form': form,
        }
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
    context = {
        'form': form,
    }

    if request.method == 'POST':
        # request.POST, username, password1, password2를 해당 이름의 변수에 할당
        # username = User가 이미 있다면 return HttpResponse 문자열로 {{usernmae}} 사용중입니다.
        # password1 / 2 가 일치하지 않는다면
        #   비밀번호와 확인란의 값이 일치하지 않습니다.
        # 3 위의 두 경우가 아니라면 새로운 유저를 생성, User로 로그인 시킨 후 post:post-list 로 리다이렉트

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            error_message = f'{username} already exists'
            context.update({'error_message': error_message, })

        elif password1 != password2:
            error_message = f'password1 and password2 do not match'
            context.update({'error_message': error_message, })
        else:
            user = User.objects.create_user(username=username, password=password1)
            login(request, user)
            return redirect('posts:post-list')

    return render(request, 'members/signup.html', context)
