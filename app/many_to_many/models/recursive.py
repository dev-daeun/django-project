from django.db import models


__all__ = (
    'FacebookUser',
)


class FacebookUser(models.Model):
    name = models.CharField(
        max_length=10,
    )
    friends = models.ManyToManyField(
        'self',
    )

    def __str__(self):
        friends_values = ', '.join(self.friends.values_list('name', flat=True))
        return f'{self.name} (친구: {friends_values})'
