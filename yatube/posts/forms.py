from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """" Форма для создания постов """
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Текст поста',
            'group': 'Группа ',
        }