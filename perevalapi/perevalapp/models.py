from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
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