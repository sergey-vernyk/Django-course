from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        # додаткові дозволи для моделі
        # permission_code, human_readable_permission_name
        permissions = [
            ("publish_post", "Can publish post"),
        ]
        # значення за замовченням

        # add_post, change_post, delete_post, view_post
        # Can add post, Can change post, Can delete post, Can view post
        default_permissions = ("add", "change", "delete", "view")

    def __str__(self) -> str:
        return str(self.title)
