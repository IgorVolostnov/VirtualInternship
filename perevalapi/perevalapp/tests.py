from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PerevalAdded, Author, PerevalImage, Coords


class PerevalAddedTest(TestCase):
    def test_create_object(self):
        user = User.objects.create(username='testuser', email='testuser@mail.ru')
        author = Author.objects.create(user=user)
        pereval = PerevalAdded.objects.create(
            beautyTitle = 'Тест1',
            title = 'Название1',
            other_titles = 'Другое название1',
            connect = 'Соединение',
            user = author,
            level_winter = 'B2',
            level_summer = 'B1',
            level_autumn = 'A2',
            level_spring = ''
        )
        Coords.objects.create(pereval=pereval,
                              latitude=12.2585,
                              longitude=65.2569,
                              height=800
                              )
        PerevalImage.objects.create(pereval=pereval,
                                    images=SimpleUploadedFile(name='test_image.jpeg',
                                                              content=open('/home/igoriusha/PycharmProjects/VirtualInternship/perevalapi/static/images/test_image.jpeg', 'rb').read(),
                                                              content_type='image/jpeg'),
                                    title='Test_image1')
        self.assertEqual(str(pereval), f"Название: {pereval.beautyTitle} {pereval.title} {pereval.other_titles}")