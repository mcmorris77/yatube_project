from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """" Форма для создания постов """
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа ',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Текст комментария',}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
