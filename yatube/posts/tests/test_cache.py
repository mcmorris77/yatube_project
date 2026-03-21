from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.cache import cache
from django.urls import reverse
from posts.models import Post, Group

User = get_user_model()

class CacheTests(TestCase):
    """Тесты кеширования главной страницы."""


    @classmethod
    def setUpClass(cls):
        """Тут создаем тестовые данные"""
        super().setUpClass()
        cls.user = User.objects.create_user(username='VladBykov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание',
        )

    def setUp(self):
        """А тут очищаем кеш перед каждым тестом"""
        cache.clear()
        self.client = Client()

    def test_index_page_caches_posts(self):
        post = Post.objects.create(
            author=self.user,
            text='Тестовый текст',
            group=self.group,
        )
        # Первый пост должен быть на главной странице
        response = self.client.get(reverse('posts:main'))
        self.assertContains(response, 'Тестовый текст')

        post.delete()

        # Проверка, что пост на месте из-за кеша
        response = self.client.get(reverse('posts:main'))
        self.assertContains(response, 'Тестовый текст')

        cache.clear()

        # Проверка, что поста нет из-за очистки кеша
        response = self.client.get(reverse('posts:main'))
        self.assertNotContains(response, 'Тестовый текст')

    def test_cache_updates_after_20_seconds(self):
        """Кеш обновляется через 20 секунд."""
        Post.objects.create(
            author=self.user,
            text='Первый пост',
        )

        # Запрос данные возвращаются в кеш
        response = self.client.get(reverse('posts:main'))
        cached_content = response.content

        # Создаём новый пост
        Post.objects.create(
            author=self.user,
            text='Второй пост',
        )

        # Запрос снова — должен вернуть закешированные данные
        response = self.client.get(reverse('posts:main'))
        self.assertEqual(response.content, cached_content)

        cache.clear()

        response = self.client.get(reverse('posts:main'))
        self.assertNotEquals(response.content, cached_content)
        self.assertContains(response, 'Второй пост')

    def tearDown(self):
        cache.clear()