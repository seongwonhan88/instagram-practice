import re

from django.db import models
from django.conf import settings

from members.forms import User


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name= '작성자',
    )
    photo = models.ImageField('사진',upload_to='post')

    # auto-now: whenever object is being called for save()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
        related_query_name='like_post',
    )

    def like_toggle(self, user):
        pass


    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    content = models.TextField('댓글 내용')

    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='태그'
        # on_delete=models.SET_NULL,
        # null=True
    )
    # Comment의 save()가 호출될 때 content의 값을 사용해서 이 필드를 자동으로 채운 후 저장하기
    _html = models.TextField('HashTag link', blank=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        def save_html():
            self._html = re.sub(
                self.TAG_PATTERN,
                r'<a href="/explore/tags/\g<tag>/">#\g<tag></a>',
                self.content
            )
        def save_tags():
            tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(self.TAG_PATTERN, self.content)]
            self.tags.set(tags)

        save_html()
        super().save(*args, **kwargs)
        save_tags()

    @property
    def html(self):
        return self._html

class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Post[{post_pk}] Like (User: {username})'.format(post_pk=self.post.pk, username=self.user.username)

    class Meta:
        unique_together=(
            ('user','post'),
        )