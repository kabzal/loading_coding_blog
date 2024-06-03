from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from django.views.decorators.cache import cache_page

from . import views

router = routers.DefaultRouter()
router.register(r'articles', views.ArticlesViewSet, basename='articles')


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('addpost/', views.AddPost.as_view(), name='add_post'),
    path('favourites/', views.FavoritePostList.as_view(), name='favourite_posts'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('add_favorite/<int:post_id>/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/<int:post_id>/', views.remove_favorite, name='remove_favorite'),
    path('remove_comment/<int:comment_id>/', views.remove_comment, name='remove_comment'),
    path('category/<slug:cat_slug>/', views.PostsCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePost.as_view(), name='edit_page'),

    # Далее - ссылки для API
    path('api/v1/', include(router.urls), name='api_posts'),
    path('api/v1/auth/', include('djoser.urls'), name='auth'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtaion_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
