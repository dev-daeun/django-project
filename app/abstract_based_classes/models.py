# 1. ABC : 자식 테이블만 존재
# 2. Multi table inheritance : 부모, 자식테이블이 모두 존재
# 3. Proxy model : 부모 테이블만 존재

from django.db import models


class CommonInfo(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,  # name 컬럼에 인덱스를 붙이는 옵션.
    )
    age = models.PositiveIntegerField(
        null=True
    )

    class Meta:
        ordering = ['name']  # ordering 대상이 되는 컬럼에는 인덱스를 붙이는 게 좋다.
        abstract = True
        # CommonInfo는 추상클래스.
        # 추상클래스 모델은 데이터베이스에 테이블을 생성하지 못하며
        # Manager를 가지지 않으므로 직접 인스턴스를 만들 수도 없다.


class Student(CommonInfo):
    home_group = models.CharField(
        max_length=5,
    )

    # CommonInfo의 Meta를 상속받는다고 명시하지 않으면 Student는 Meta를 새로 덮어씌우므로
    # CommonInfo의 메타 옵션을 쓸 수 없다. => 메타클래스를 상속받는다고 명시해야 됨.
    class Meta(CommonInfo.Meta):
        # 데이터베이스의 테이블 이름을 직접 지을 수 있음.
        db_table = 'student'
        verbose_name = '학생'
        verbose_name_plural = '학생 목록'

    def __str__(self):
        return self.name
