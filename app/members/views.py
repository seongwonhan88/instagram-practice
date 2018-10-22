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
    if request.method == 'POST':
        pass
    else:

        form = SignupForms()
        context = {
            'form':form,
        }

        return render(request, 'members/signup.html', context)