from django.db import models


class User1Manager(models.Manager):
    def normal_users(self):
        return super().get_queryset().filter(is_admin=False)

    def admin_users(self):
        return super().get_queryset().filter(is_admin=True)


class User1(models.Model):
    name = models.CharField(
        max_length=30,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    # 기본 매니저를 User1Manager의 인스턴스로 덮어씌움. => 매니저 커스터마이징.
    # 커스텀 매니저에 메소드를 정의하면 이 매니저를 통해 메소드를 호출할 수 있다.
    objects = User1Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Inheritance_Proxy_User1'


class UtilMixin(models.Model):

    @classmethod
    def show_items(cls):
        print(f' - Model({cls.__name__}) items - ')
        for item in cls._default_manager.all():
            print(item)

    def set_name(self, new_name):
        old_name = self.name
        self.name = new_name
        self.save()
        print(f'{self.__class__.__name__} instance name change ({old_name}, {new_name})')

    class Meta:
        abstract = True


class NormalUser1Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=False)


class AdminUser1Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)

    # UtilMixin을 상속받았으므로 UtilMixin의 모든 메서드를 갖는다.
    # 어떤 클래스들이 UtilMixin처럼 모델 필드를 가지지 않는다면,(메서드만 갖는다면) 프록시모델은 얼마든지 그 클래스들을 상속받을 수 있다.
    # 모델 필드는 곧 물리적 테이블의 컬럼이므로 필드가 있는 클래스를 다중으로 상속받을 수 없는 것과 같은 맥락.
    # 예) UtilMixin는 필드는 없고 메소드만 있음. => NormalUser에서 User1과 같이 상속받을 수 있다.


class NormalUser(UtilMixin, User1):
    objects = NormalUser1Manager()

    def find_user(self, name):
        return User1.objects.filter(name__contains=name)

    class Meta:
        proxy = True


class Admin(UtilMixin, User1):
    objects = AdminUser1Manager()

    def delete_user(self, user):
        user.delete()

    class Meta:
        proxy = True
