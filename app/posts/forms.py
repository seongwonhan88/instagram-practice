from django import forms


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
