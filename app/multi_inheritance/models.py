from django.db import models


def get_removed_place():
    try:
        place = Place.objects.get(name='철거됨')
    except Place.DoesNotExist:
        place = Place.objects.create(name='철거됨')
    finally:
        return place


class Place(models.Model):
    name = models.CharField(
        max_length=10,
    )
    address = models.CharField(
        max_length=10,
    )

    def __str__(self):
        return f'{self.name} [Place]'


# Place 클래스를 상속 받음. => Restaurant의 name, address는 Place테이블에 들어감. => 조인을 해야된다.

class Restaurant(Place):
    # 상속을 받으면 암시적으로 일대일 필드가 생김. default : <부모클래스소문자_ptr>
    # place_ptr = models.OneToOneField(<Place>)

    # 부모클래스 필드를 커스텀하고 싶으면 필드를 만들고 parent_link=True 옵션을 준다.
    # 가게의 이전 주소가 없어질 경우(현실에서는 건물이 없어진다거나 할 때)
    # '철거됨'이라는 Place의 row가 필요하다
    # models.SET 함수는 callable한 함수를 인자로 받아서 그 함수의 결과를 row로 정한다.
    place_ptr_customized = models.OneToOneField(
        Place,
        parent_link=True,
        primary_key=True,
        on_delete=models.SET(get_removed_place),
        related_name='restaurants',
        related_query_name='restaurant',
    )
    serve_hot_dogs = models.BooleanField(
        default=False,
    )
    serve_pizza = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.name} [Restaurant]'

