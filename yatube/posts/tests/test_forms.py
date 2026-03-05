from django.template.defaultfilters import title
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()

class PostCreateFormTest(TestCase):
    """Тесты формы создания поста"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()


        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.user = User.objects.create_user(username='VladBykov')

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_valid_form_creates_new_post(self):
        """При отправке валидной формы создаётся новый пост в БД."""

        post_count = Post.objects.count()

        form_data = {
            'text': 'Новый тестовый пост',
            'group': self.group.id,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), post_count + 1)
        new_post = Post.objects.latest('pub_date')
        self.assertEqual(new_post.text, 'Новый тестовый пост')
        self.assertEqual(new_post.group, self.group)
        self.assertEqual(new_post.author, self.user)

    def test_valid_form_edits_existing_post(self):
        """При отправке валидной формы происходит изменение поста в БД."""

        post = Post.objects.create(
            author=self.user,
            text='Оригинальный текст',
            group=self.group,
        )

        from_data = {
            'text': 'Измененный текст',
            'group': self.group.id,
        }
        response = self.client.post(
            reverse('posts:post_edit', kwargs={'pk': post.pk}),
            data=from_data,
            follow=True

        )

        # ✅ Проверяем что пост был изменён
        updated_post = Post.objects.get(pk=post.pk)
        self.assertEqual(updated_post.text, 'Измененный текст')

        # ✅ Проверяем что количество постов не изменилось
        self.assertEqual(Post.objects.count(), 1)
