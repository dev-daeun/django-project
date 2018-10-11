from django.db import models
from django.utils import timezone

___all__ = (
    'TwitterUser',
    'Relation',
)


class TwitterUser(models.Model):
    """
    내가 팔로우하는 유저 : following
    나를 팔로우하는 유저 : follower
    내가 블락한 유저 : block_list

    특정 유저가 다른 유저를
    follow (팔로우)
    block  (차단)

    intermediate 모델이 갖는 정보는
    - from_user : 팔로-팔로잉 관계를 만든 유저
    - to_user : 만든 관계에 대상이 되는 유저
    - relation_type : follow 또는 block


    """
    name = models.CharField(
        max_length=20,
    )
    relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    def __str__(self):
        return self.name

    @property
    def followers(self):
        """
        :return: 나를 팔로우하는 다른 트위터유저 쿼리셋
        """
        return TwitterUser.objects.filter(
            from_user_relations__to_user=self,
            from_user_relations__relation_type='f',
        )

    @property
    def follwing(self):
        """
        :return: 내가 팔로우하는 다른 트위터유저 쿼리셋
        """
        return TwitterUser.objects.filter(
            to_user_relation__from_user=self,
            to_user_relation__relation_type='f',
        )

    @property
    def block_list(self):
        """
        :return: 내가 블락한 다른 트위터유저 쿼리셋
        """
        return TwitterUser.objects.filter(
            to_user_relation__from_user=self,
            to_user_relation__relation_type='b',
        )

    @property
    def follower_relations(self):
        """
        :return: 나를 follow하는 Relation QuerySet
        """
        return self.to_user_relations.filter(
            relation_type='f',
        )

    @property
    def followee_relations(self):
        """
        :return: 내가 follow하는 Relation QuerySet
        """
        return self.from_user_relations.filter(
            relation_type='f',
        )

    def follow(self, user):
        """
        다른 트위터유저 팔로우
        1. 이미 존재하면 만들지 않는다.
        2. 유저가 block_list에 속한다면 만들지 않는다.
        :param user: TwitterUser
        :return:
        """
        if not self.from_user_relations.filter(to_user=user).exists():
            self.from_user_relations.create(
                to_user=user,
                relation_type='f',
            )
        return self.from_user_relations.get(to_user=user)

    def block(self, user):
        """
        트위터유저 블락
        :param user:
        :return:
        """
        try:
            relation = self.from_user_relations.get(to_user=user)
            if relation.relation_type == 'f':
                relation.relation_type = 'b'
                relation.created_at = timezone.now()
                relation.save()
        except Relation.DoesNotExist:
            relation = self.from_user_relations.create(
                to_user=user,
                relation_type='b'
            )
        finally:
            return relation


class Relation(models.Model):
    CHOICE_RELATION_TYPE = (
        ('f', 'Follow'),
        ('b', 'Block'),
    )
    # 같은 모델 TwitterUser를 두 개 이상의 필드에서 참조하려고하면
    # TwitterUser에서 역방향으로 relation_set에 접근하려고 할 때
    # 본인이 from_user 입장인지, to_user 입장인지 알 수 없다. 따라서 충돌이 발생함.
    # relation_name으로 구분지어야 됨.
    from_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_user_relation',
    )
    to_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_user_relation',

        # related_query_name
        # 디폴트 : related_name
        # 다대다로 연결된 다른 테이블의 속성을 검색할 때 filter(key=value) 로 쓰는데,
        # key에 다른 특정 테이블을 가리키고 싶을 대 다대다필드를 정의한 테이블(소스테이블)의 경우에는 해당 필드명을 쓴다. 예) Group => members 로 명명.
        #
    )
    relation_type = models.CharField(
        choices=CHOICE_RELATION_TYPE,
        max_length=1,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )
