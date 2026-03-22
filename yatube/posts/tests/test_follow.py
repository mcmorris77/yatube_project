from django.contrib.auth import get_user_model
from posts.models import Post, Follow
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()

class FollowTest(TestCase):
    # Тесты системы подписок
    def setUp(self):
        self.user = User.objects.create_user(username='VladBykov')
        self.author = User.objects.create_user(username='testauthor')

        self.client = Client()
        self.client.force_login(self.user)


    def test_follow_unfollow(self):
        # Подписка
        self.client.get(reverse('posts:profile_follow', args=[self.author.username]))
        self.assertEqual(Follow.objects.count(), 1)

        # Отписка
        self.client.get(reverse('posts:profile_unfollow', args=[self.author.username]))
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_index(self):
        Follow.objects.create(user=self.user, author=self.author)

        post = Post.objects.create(author=self.author, text='текст')

        response = self.client.get(reverse('posts:follow_index'))
        self.assertIn(post, response.context['page_obj'])

        other_user = User.objects.create(username='other')
        self.client.force_login(other_user)

        response = self.client.get(reverse('posts:follow_index'))
        self.assertNotIn(post, response.context['page_obj'])
