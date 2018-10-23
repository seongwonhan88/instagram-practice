from django.shortcuts import redirect


def index(reqeust):
    return redirect('posts:post-list')