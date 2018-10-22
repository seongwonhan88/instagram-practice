from django.shortcuts import render, redirect

# from members.models import User
from .forms import PostCreateForm
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
    # 1. posts/post_create.html
    # form is
    # button[type=submit]
    # input[type=file]

    # 2. /posts/create/URL -> view 연결
    # 3. render사용해서 template return
    # 4. base.html nav부분에 '+add post' 텍스트 갖는 a link 추가
    # 5  {% url %} tag 사용해서 포스트 생성으로 링크 걸어주기
    if request.method == 'POST':
        Post.objects.create(
            author=request.user,
            photo=request.FILES['photo'], )
        return redirect('posts:post-list')
    else:
        # get 요청의 경우 빈 Form 인스턴스를 context에 담아서 저달
        # template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능

        form = PostCreateForm()
        context = {
            'form': form,
        }

        return render(request, 'posts/post_create.html', context)
