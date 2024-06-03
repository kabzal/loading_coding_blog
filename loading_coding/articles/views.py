from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from rest_framework.decorators import action
from rest_framework.response import (Response)
from rest_framework import viewsets

from articles.forms import AddPostForm, ContactForm, CommentAddForm
from articles.models import Posts, Tag, Category, Comment, Contact
from articles.permissions import IsOwnerOrReadOnly
from articles.serializers import PostsSerializer
from articles.utils import DataMixin


# Главная страница (статьи)
class HomePage(DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    title_page = 'Все статьи'
    cat_selected = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_posts = Posts.published.order_by('-read_num')[:5]
        context['popular_posts'] = popular_posts
        return context

    def get_queryset(self):
        posts_lst = cache.get('posts')
        if not posts_lst:
            posts_lst = Posts.published.all().select_related('cat')
            cache.set('posts', posts_lst, 60)
        return posts_lst


# Страница с текстом выбранной статьи и комментариями к ней
class ShowPost(LoginRequiredMixin, DataMixin, DetailView):
    template_name = 'articles/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentAddForm() # Форма добавления нового комментария
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        post = get_object_or_404(Posts.published, slug=self.kwargs[self.slug_url_kwarg])
        # При открытии статьи счетчик просмотров увеличивается на 1
        post.read_num += 1
        post.save()
        return post

    def post(self, request, *args, **kwargs):
        # Срабатывает POST-запрос в случае, если была заполнена и отправлена
        # форма создания нового комментария
        post = self.get_object()
        self.object = post
        form = CommentAddForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.commenter = request.user
            new_comment.save()
            return self.render_to_response(self.get_context_data(comment_form=form))
        else:
            return self.render_to_response(self.get_context_data())


# Класс представления для добавления новой статьи
class AddPost(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'articles/addpost.html'
    title_page = "Добавление статьи"
    permission_required = 'articles.add_posts'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.author = self.request.user
        return super().form_valid(form)


# Класс представления для редактирования статьи
class UpdatePost(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Posts
    fields = ('title', 'content', 'photo', 'is_published', 'cat')
    template_name = 'articles/addpost.html'
    success_url = reverse_lazy('home')
    title_page = "Редактирование статьи"
    permission_required = 'articles.change_posts'


# Страница с формой обратной связи, сохраняющая обращение пользователя в БД
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'articles/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        data = form.cleaned_data
        contact = Contact.objects.create(
            name=data['name'],
            email=data['email'],
            content=data['content']
        )
        return super().form_valid(form)


# Отображение статей по выбранной категории
class PostsCategory(DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Posts.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        popular_posts = Posts.published.order_by('-read_num')[:5]
        context['popular_posts'] = popular_posts
        return self.get_mixin_context(context, title='Категория: ' + cat.name, cat_selected=cat.pk)


# Отображение статей по выбранному тегу
class TagPostList(DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        popular_posts = Posts.published.order_by('-read_num')[:5]
        context['popular_posts'] = popular_posts
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Posts.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


# Отображение избранных статей
class FavoritePostList(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'articles/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_posts = Posts.published.order_by('-read_num')[:5]
        context['popular_posts'] = popular_posts
        return self.get_mixin_context(context, title='Ваши избранные статьи')

    def get_queryset(self):
        user = self.request.user
        return user.favorite_posts.all()


# Добавление статьи в Избранное
@login_required
def add_favorite(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.favorited_by.add(request.user)
    return redirect(reverse('post', kwargs={'post_slug': post.slug}))


# Удаление статьи из Избранных
@login_required
def remove_favorite(request, post_id):
    post = get_object_or_404(Posts, pk=post_id)
    post.favorited_by.remove(request.user)
    return redirect(reverse('post', kwargs={'post_slug': post.slug}))


# Удаление комментария
@login_required
def remove_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_slug = comment.post.slug
    if comment.commenter == request.user or request.user.is_staff:
        comment.delete()
        return redirect(reverse('post', kwargs={'post_slug': post_slug}))
    else:
        redirect(reverse('post', kwargs={'post_slug': post_slug}))


# Обработка ненайденной страницы (ошибка 404)
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Ошибка 404: Страница не найдена.<br>Попробуйте проверить ссылку</h1>')


# <----------! Представления для API !---------->


# Доступ к опубликованным статьям с помощью API
class ArticlesViewSet(viewsets.ModelViewSet):
    serializer_class = PostsSerializer
    permission_classes = (IsOwnerOrReadOnly, ) # Разрешение только для админа и автора статьи

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Posts.published.all()

        return Posts.published.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def category_list(self, request, pk=None):
        if pk:
            cat = Category.objects.get(pk=pk)
            return Response({'cat': cat.name})
        else:
            cats = Category.objects.all()
            return Response({'cats': [c.name for c in cats]})

