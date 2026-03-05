from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.template.defaultfilters import title
from django.test import TestCase, Client
from posts.models import Post, Group

User = get_user_model()

class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Создаём тестовые данные один раз для всех тестов класса.
        Выполняется перед запуском всех тестов.
        """

        super().setUpClass()

        # Создаем пользователя автора поста
        cls.user = User.objects.create_user(username='testuser')

        # Создаём другого пользователя (не автора)
        cls.other_user = User.objects.create_user(username='otheruser')

        # Создаем группу
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )


        # Создаем пост
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )

    def setUp(self):
        """
        Создаём тестовые клиенты перед каждым тестом.
        Выполняется перед каждым тестом.
        """

        self.guest_client = Client()

        # Авторизованный клиент(автор)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        # Авторизованный клиент (не автор)
        self.other_client = Client()
        self.other_client.force_login(self.other_user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        url_templates = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user.username}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
        }
        for url, template in url_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """Страницы доступны любому пользователю."""
        # Список URL, доступных всем
        public_urls = {
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.pk}/',
        }

        for url in public_urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')


    def test_create_url_exists_at_desired_location_authorized(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_redirect_anonymous(self):
        """Страница редактирования перенаправляет анонимного пользователя."""
        response = self.guest_client.get(
            f'/posts/{self.post.pk}/edit/',
            follow=True,
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.pk}/edit/'
        )

    def test_post_edit_url_redirect_not_author(self):
        """Страница редактирования перенаправляет не-автора на просмотр поста."""
        response = self.other_client.get(
            f'/posts/{self.post.pk}/edit/',
            follow=True,
        )
        self.assertRedirects(
            response,
            f'/posts/{self.post.pk}/',
        )

    def test_post_edit_url_exists_at_desired_location_author(self):
        """Страница редактирования доступна автору поста."""
        response = self.authorized_client.get(
            f'/posts/{self.post.pk}/edit/',
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting_page_returns_404(self):
        """Запрос к несуществующей странице вернёт ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)






class StaticURLTests(TestCase):
    def test_homepage(self):
        # Создаем экземпляр клиента
        guest_client = Client()
        # Делаем запрос к главной странице и проверяем статус
        response = guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)


