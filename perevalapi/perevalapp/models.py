from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

tz = timezone.get_default_timezone()


class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'авторы'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Автор')
    fam = models.CharField(max_length=255, blank=False, verbose_name='Фамилия автора')
    name = models.CharField(max_length=255, blank=False, verbose_name='Имя автора')
    otc = models.CharField(max_length=255, blank=False, verbose_name='Отчество автора')
    phone = models.CharField(max_length=255, blank=False, verbose_name='Телефон автора')


    def __str__(self):
        return self.user.username


class PerevalAreas(models.Model):
    class Meta:
        verbose_name = 'Территория перевала'
        verbose_name_plural = 'Территории перевалов'

    id_parent = models.IntegerField(default=0, verbose_name='Номер родителя')
    title = models.TextField(blank=False, verbose_name='Название территории')

    def __str__(self):
        return self.title


class PerevalAdded(models.Model):
    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    KIND_STATUS = [
        ('new', 'Новый'),
        ('pending', 'В работе'),
        ('accepted', 'Успешно'),
        ('rejected', 'Отказано')
    ]

    beautyTitle = models.CharField(max_length=255, blank=False, verbose_name='Красивое название')
    title = models.CharField(max_length=255, blank=False, verbose_name='Название')
    other_titles = models.CharField(max_length=255, blank=False, verbose_name='Другое название')
    connect = models.CharField(max_length=255, default="", blank=True, verbose_name='Соединение')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='pereval', verbose_name='Автор')
    level_winter = models.CharField(max_length=255, default="", blank=True, verbose_name='Уровень зимой')
    level_summer = models.CharField(max_length=255, default="", blank=True, verbose_name='Уровень летом')
    level_autumn = models.CharField(max_length=255, default="", blank=True, verbose_name='Уровень осенью')
    level_spring = models.CharField(max_length=255, default="", blank=True, verbose_name='Уровень весной')
    status = models.CharField(choices=KIND_STATUS, default="new", blank=True, verbose_name='Статус')

    def __str__(self):
        return f"Название: {self.beautyTitle} {self.title} {self.other_titles}"


class Coords(models.Model):
    class Meta:
        verbose_name = 'Координаты перевала'
        verbose_name_plural = 'Координаты перевалов'

    latitude = models.FloatField(default=0.0, null=True, verbose_name='Широта перевала')
    longitude = models.FloatField(default=0.0, null=True, verbose_name='Долгота перевала')
    height = models.IntegerField(default=0, null=True, verbose_name='Высота перевала')
    pereval = models.ForeignKey(PerevalAdded, default=None, on_delete=models.CASCADE, related_name='coordinates',
                                verbose_name='Перевал')

    def __str__(self):
        return f"Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}"


class PerevalImage(models.Model):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    pereval = models.ForeignKey(PerevalAdded, default=None, on_delete=models.CASCADE, related_name='photos',
                                verbose_name='Перевал')
    images = models.ImageField(upload_to = 'images', verbose_name='Изображение')
    title = models.TextField(blank=False, verbose_name='Название изображения')

    def __str__(self):
        return f'id: {self.pk}, title: {self.title}'