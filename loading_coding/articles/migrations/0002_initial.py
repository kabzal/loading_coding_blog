# Generated by Django 5.0.3 on 2024-03-24 12:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='posts',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='articles.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='posts',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='articles.tag', verbose_name='Теги'),
        ),
        migrations.AddIndex(
            model_name='posts',
            index=models.Index(fields=['time_update'], name='articles_po_time_up_19e90e_idx'),
        ),
    ]
