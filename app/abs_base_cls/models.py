from django.db import models

__all__ = (
    'Person',
    'PhotoPost',
    'TextPost',
)


class Person(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name


class PostBase(models.Model):
    author = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        # PostBase를 상속받은 클래스의 이름을 소문자로 바꾼 것이 related_name으로 들어감.
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)s",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class TextPost(PostBase):
    text = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f'text-post author: {self.author.name}'


class PhotoPost(PostBase):
    photo_url = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return f'photo-post author: {self.author.name}'
