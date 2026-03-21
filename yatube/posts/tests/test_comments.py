'''Задание 2
Напишите тесты, которые проверяют, что
* комментировать посты может только авторизованный пользователь;
* после успешной отправки комментарий появляется на странице поста.'''
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Group
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()

class CommentTests(TestCase):
    "Тесты системы комментариев"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.user = User.objects.create_user(username='VladBykov')

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост для комментариев',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_authorized_user_can_comment(self):
        """Авторизованный пользователь может комментировать."""
        comments_count = Comment.objects.count()
        form_data = {'text': 'Тестовый комментарий'}
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'pk': self.post.pk}),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'pk': self.post.pk})
        )

        self.assertEqual(Comment.objects.count(), comments_count + 1)

        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий',
                post=self.post,
                author=self.user,
            ).exists()
        )


    def test_guest_cannot_comment(self):
        """Неавторизованный пользователь НЕ может комментировать."""
        comments_count = Comment.objects.count()

        form_data = {'text': 'Комментарий от гостя'}

        response = self.guest_client.post(
            reverse('posts:add_comment', kwargs={'pk': self.post.pk}),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.pk}/comment/'
        )

        self.assertEqual(Comment.objects.count(), comments_count)

    def test_comment_appears_on_post_page(self):
        """После отправки комментарий появляется на странице поста."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Новый комментарий',
        )

        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'pk': self.post.pk})
        )

        self.assertIn(comment, response.context['comments'])
        self.assertContains(response, 'Новый комментарий')