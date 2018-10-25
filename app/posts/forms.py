from django import forms

from .models import Post, Comment


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False,
    )

    def save(self, **kwargs):
        if self.errors:
            raise ValueError('Post validation failed')
        post = Post.objects.create(photo=self.cleaned_data['photo'], **kwargs)
        # comment 항목이 있다면, 생성한 Post에 연결되는 comment 를 생성
        # post=post, author=request.user
        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            post.comments.create(
                author = post.author,
                content=comment_content,
            )
        # post_list 에서 댓글 목록 출력r
        return post

class CommentCreateForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows': 2,
            }
        ),
    )

    def save(self, post, **kwargs):
        post.comments.create(**kwargs)
        content = self.cleaned_data['content']
        return post.comments.create(
            content=content,
            **kwargs
        )
