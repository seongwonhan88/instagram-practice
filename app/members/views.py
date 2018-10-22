from django.shortcuts import render
from .forms import LoginForms


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
        pass
    else:
        form = LoginForms()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)
