from rest_framework import serializers

from articles.models import Posts


class PostsSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Posts
        fields = ("title", "slug", "content", "time_create",
                  "time_update", "is_published", "cat",
                  "tags", "read_num", "author")
