import re

from django.db import models
from django.conf import settings

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

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tags = [HashTag.objects.get_or_create(name=name)[0] for name in re.findall(self.TAG_PATTERN, self.content)]
        self.tags.set(tags)

    @property
    def html(self):
        #자신의 컨텐츠 속성값에서 #문자열을
        substitutes = []
        pattern = re.compile(r'#(?P<tag_name>\w+)')
        string = re.sub(pattern, r'<a href="./explore/tags/\g<tag_name>/">#\g<tag_name></a>', self.content)
        # for item in string_origin:
        #     # substitutes.append(self.TAG_PATTERN.sub(f'<a href="/explore/tags/{item[1:]}">{item}</a>',item))
        #     substitutes.append(pattern.sub('<a href="./explore/tags/g<tag_name>"></a>'.format(item[1:],item),item))
        # string_hashtag = ' '.join(substitutes)
        return string

class HashTag(models.Model):
    name = models.CharField('태그명', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'