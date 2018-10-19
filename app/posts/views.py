from django.shortcuts import render

from .models import Post


def post_list(request):
    # 1. Post 모델에 created_at(생성시간)
    # modified_at(수정시간)
    # 두 필드 추가

    # 2. Post 모델이 기본적으로 pk내림차순으로 정렬되도록 설정
    # 3. 모든 포스트 객체에 대한 쿼리셋을 render의 인수로 전달

    posts = Post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'posts/post_list.html', context)

def post_create(request):
    #1. posts/post_create.html
    # form is
    # button[type=submit]
    # input[type=file]

    #2. /posts/create/URL -> view 연결
    #3. render사용해서 template return
    #4. base.html nav부분에 '+add post' 텍스트 갖는 a link 추가
    #5  {% url %} tag 사용해서 포스트 생성으로 링크 걸어주기

    return render(request, 'posts/post_create.html')
