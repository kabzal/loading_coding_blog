from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISHED)


# модель с основной информацией
class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name="Заголовок")
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True,
                            verbose_name='Слаг',
                            validators=[
                                MinLengthValidator(5, message="Минимум 5 символов"),
                                MaxLengthValidator(100, message="Максимум 100 символов")
                            ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",
                              default=None,
                              blank=True,
                              null=True,
                              verbose_name="Фото")

    content = models.TextField(blank=True,
                               verbose_name="Полный текст")
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Время создания статьи")
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name="Время обновления")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT,
                                       verbose_name="Статус публикации")
    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT,
                            related_name='posts',
                            verbose_name="Категории")
    tags = models.ManyToManyField('Tag',
                                  blank=True,
                                  related_name='tags',
                                  verbose_name="Теги")
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               null=True,
                               default=None,
                               related_name='posts',
                               verbose_name="Автор")
    read_num = models.IntegerField(default=0,
                                   verbose_name="Количество просмотров")
    favorited_by = models.ManyToManyField(get_user_model(),
                                          blank=True,
                                          related_name="favorite_posts",
                                          verbose_name="Избранное")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f'Статья "{self.title}"'

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = verbose_name
        ordering = ['-time_update']
        indexes = [
            models.Index(fields=['time_update'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=150,
                            db_index=True,
                            verbose_name="Наименование категории")
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Tag(models.Model):
    tag = models.CharField(max_length=100,
                           db_index=True)
    slug = models.SlugField(max_length=255,
                            db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


class Comment(models.Model):
    post = models.ForeignKey(Posts,
                             on_delete=models.CASCADE,
                             related_name='comments')
    commenter = models.ForeignKey(get_user_model(),
                                  on_delete=models.CASCADE,
                                  related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Комментарий пользователя {self.commenter.username} к посту {self.post.title}'


class Contact(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Имя обратившегося")
    email = models.EmailField(verbose_name="Email")
    content = models.TextField(blank=True,
                               verbose_name="Текст обращения")
    created = models.DateTimeField(auto_now=True,
                                   verbose_name="Дата обращения")
    viewed = models.BooleanField(default=False,
                                 verbose_name='Просмотрено')

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f"Обращение №{self.id} от {self.name}"