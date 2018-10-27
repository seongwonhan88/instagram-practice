import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CommentForm, PostForm
from .models import Post, HashTag, PostLike


def tag_search(request):
    search_keyword = request.GET.get('search_keyword')
    substitute_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substitute_keyword)


def tag_post_list(request, tag_name):
    posts = Post.objects.filter(comments__tags__name__exact=tag_name).distinct()
    context={
        'posts':posts,
    }
    return render(request, 'posts/tag_post_list.html', context)

def post_list(request):
    # 1. Post 모델에 created_at(생성시간)
    # modified_at(수정시간)
    # 두 필드 추가

    # 2. Post 모델이 기본적으로 pk내림차순으로 정렬되도록 설정
    # 3. 모든 포스트 객체에 대한 쿼리셋을 render의 인수로 전달

    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }

    return render(request, 'posts/post_list.html', context)

@login_required
def post_create(request):
    context = {}
    # view 에서 User가 로그인 상태가 아니면
    # post:post-list로 리다이렉트

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            comment_content = form.cleaned_data['comment']

            #comment가 가진 content 속성에서 해시태그에 해당하는 문자열을 가져와서 HashTag객체를 가져오거나 생성
            # (get or create)
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=comment_content
                )
            return redirect('posts:post-list')
    else:
        # get 요청의 경우 빈 Form 인스턴스를 context에 담아서 저달
        # template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능
        form = PostForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    """
    post_pk에 해당하는 Post에 댓글을 생성하는 view
    'POST'메스트 요청만 처리

    'content'키로 들어온 값을 사용해 댓글 생성. 작성자는 요청한 User
    URL: /posts/<post_pk>/comments/create

    댓글 완성 후엔 posts:post-list로 redirect
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post-list')

def post_like_toggle(request, post_pk):
    # url : 'posts/postpk/like-toggle/
    # url name : posts:post-like-toggle
    # post method only

    # request.user 가 postpk에 해당하는 post에 like toggle처리
    if request.method == 'POST':
        post = Post.objects.all()
        post_like = PostLike.objects.filter(user=request.user, post_id=post_pk)
        if Post.objects.filter(pk=post_pk, like_users=request.user).exists():
            post_like.delete()
        else:
            PostLike.objects.filter(user=request.user, post_id=post_pk).create()

    context={'post': post, 'post_like':post_like}
    return render(request, 'posts/post_list.html', context)