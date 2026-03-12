from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import PostForm


User = get_user_model()

def index(request):
    """Главная страница"""
    post_list = Post.objects.all().order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    """Страница группы с постами"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    """Профиль пользователя"""
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author', 'group').all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,      # Объект пользователя
        'page_obj': page_obj   # Объект страницы с постами
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, pk):
    """Детали поста"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'),
        pk=pk
    )
    
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Создание нового поста."""

    if request.method == 'POST':
        # Пользователь отправил форму
        form = PostForm(
            request.POST,
            files=request.FILES or None  # ← ДОБАВЛЕНО!
        )

        if form.is_valid():
            # Форма заполнена правильно
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)

        # Если форма НЕ валидна, код продолжится и покажет форму с ошибками

    else:
        # Пользователь просто открыл страницу
        form = PostForm()

    # Показываем форму (пустую или с ошибками)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, pk):
    """
    Редактирование существующего поста.
    Доступно только автору поста.
    """
    # Получаем пост по ID
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        # Проверяем является ли пользователь автором поста
        return redirect('posts:post_detail', pk=post.pk)


    if request.method == 'POST':
        # Пользователь отправил форму с изменениями
        # instance=post — говорим форме, какой пост редактируем
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )

        if form.is_valid():
            # Сохраняем изменения
            form.save()
            # Отправляем на страницу этого поста
            return redirect('posts:post_detail', pk=pk)
    else:
        # Пользователь открыл страницу редактирования
        # Создаём форму, заполненную данными поста
        form = PostForm(instance=post)

    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)