from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from articles.models import Posts


class GetPostsTestCase(TestCase):

    fixtures = [
        "all_data.json",
    ]

    def setUp(self):
        "Инициализируется перед выполнением каждого теста"

    def test_home_page(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'articles/index.html')
        self.assertEqual(response.context_data['title'], "Все статьи")

    def test_data_home_page(self):
        posts = Posts.published.all().select_related('cat').order_by('-time_update')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], posts[:3])

    def test_redirect(self):
        path = reverse('add_post')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_paginate_homepage(self):
        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f"?page={page}")
        posts = Posts.published.all().select_related('cat').order_by('-time_update')
        print(posts[(page - 1) * paginate_by:page * paginate_by])
        print(response.context_data['posts'])
        self.assertQuerySetEqual(response.context_data['posts'],
                                 posts[(page-1) * paginate_by:page * paginate_by])

    def test_post_redirect(self):
        post = Posts.published.get(pk=1)
        path = reverse('post', args=[post.slug])
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def tearDown(self):
        "Действия после выполняния каждого теста"
