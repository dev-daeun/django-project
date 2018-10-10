from django.db import models


# __all__ : 외부에서 모듈 import * 할 때 *의 대상이 되는 목록.
__all__ = (
    'InstagramUser',
)


class InstagramUser(models.Model):
    name = models.CharField(
        max_length=50,
    )
    # 내가 팔로우하는 유저 : following
    # 나를 팔로우하는 유저 : follower
    # following 필드는 내가 팔로우 하는 사람을 나타냄.
    # 팔로우 당하는 입장에서 객체는 자기의 followers에 접근하려면 related_name으로 접근한다.

    # symmetrical : 릴레이션 테이블에서 비대칭/대칭관계 설정.
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
    )

    def __str__(self):
        return self.name
