from django import forms

from .models import Post


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
        return post
