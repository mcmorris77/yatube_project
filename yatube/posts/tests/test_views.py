from unittest import expectedFailure

from django.contrib.auth import get_user_model
from django.template.defaultfilters import title
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()

class PostViewsTest(TestCase):
    """Тесты view-функций приложения posts."""

    @classmethod
    def setUpClass(cls):
        """Создаём тестовые данные один раз для всего класса"""
        super().setUpClass()

        cls.user = User.objects.create_user(username='VasyaVpiska')

        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание группы',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group,
        )

    def setUp(self):
        """Создаём клиентов перед каждым тестом"""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/index.html': reverse('posts:main'),
            'posts/group_list.html': reverse('posts:group_list',
                                             kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse('posts:profile',
                                          kwargs={'username': 'VasyaVpiska'}),
            'posts/post_detail.html': reverse('posts:post_detail',
                                         kwargs={'pk': self.post.pk}),
            'posts/create_post.html': reverse('posts:post_create'),

        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:main'))
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['page_obj'][0], self.post)

    def test_group_list_page_show_correct_context(self):
        """На странице группы в контексте есть group и posts."""
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        group = response.context['group']
        group_data={
            'title': group.title,
            'slug': group.slug,
        }
        expected_group={
            'title': 'Тестовая группа',
            'slug': 'test-slug',
        }
        self.assertEqual(group_data, expected_group)
        self.assertIn(self.post, response.context['posts'])

    def test_post_detail_context_contains_post(self):
        """На странице поста в контексте есть post с правильными данными."""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'pk': self.post.pk})
        )
        post = response.context['post']
        post_data={
            'author': post.author,
            'text': post.text,
            'group': post.group,
        }
        expected_post={
            'author': self.post.author,
            'text': self.post.text,
            'group': self.post.group,
        }
        self.assertEqual(post_data, expected_post)

    def test_post_create_form_has_correct_fields(self):
        """На странице создания поста форма имеет правильные типы полей."""
        response = self.authorized_client.get(reverse('posts:post_create'))

        form_fields={
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for field_name, expected_type in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = response.context['form'].fields[field_name]
                self.assertIsInstance(form_field, expected_type)



































