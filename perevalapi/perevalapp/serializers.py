from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    created = serializers.HiddenField(default=timezone.now, source='user.date_joined')
    class Meta:
        model = Author
        fields = ['id', 'fam', 'name', 'otc', 'user', 'phone', 'created']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        try:
            user = User.objects.get(email=user_data.get('email'))
        except User.DoesNotExist:
            user = User.objects.create(**user_data)
        instance = Author.objects.create(user=user, **validated_data)
        instance.save()
        return instance


class CoordsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Coords
        fields = ['id', 'latitude', 'longitude', 'height']
        read_only_fields = ['id']

    def to_representation(self, obj):
        return {
            'id': obj.pk,
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'height': obj.height
        }

class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = PerevalImage
        fields = ('id', 'title', 'images')
        read_only_fields = ['id']

    def to_representation(self, obj):
        return {
            'id': obj.pk,
            'title': obj.title
        }


class PerevalAddedSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.ReadOnlyField(source='user.user.username')
    email = serializers.ReadOnlyField(source='user.user.email')
    fam = serializers.ReadOnlyField(source='user.fam')
    name = serializers.ReadOnlyField(source='user.name')
    otc = serializers.ReadOnlyField(source='user.otc')
    phone = serializers.ReadOnlyField(source='user.phone')
    coordinates = CoordsSerializer(many=True)
    photos = ImageSerializer(many=True)
    class Meta:
        model = PerevalAdded
        fields = ['beautyTitle', 'title', 'other_titles', 'connect', 'add_time', 'username', 'email', 'fam', 'name',
                  'otc', 'phone', 'coordinates', 'level_winter', 'level_summer', 'level_autumn', 'level_spring',
                  'photos']
        extra_fields = ['status']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(PerevalAddedSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        user_data = author_data.get('user')
        coords_data = validated_data.pop('coordinates')
        images_data = self.context.get('view').request.FILES
        user = User.objects.create(**user_data)
        author = Author.objects.create(user=user, fam=author_data.get('fam'), name=author_data.get('name'),
                                       otc=author_data.get('otc'), phone=author_data.get('phone'))
        instance = PerevalAdded.objects.create(user=author,
                                               beautyTitle=validated_data.get('beautyTitle'),
                                               title=validated_data.get('title'),
                                               other_titles=validated_data.get('other_titles'),
                                               connect=validated_data.get('connect'),
                                               level_winter=validated_data.get('level_winter'),
                                               level_summer=validated_data.get('level_summer'),
                                               level_autumn=validated_data.get('level_autumn'),
                                               level_spring=validated_data.get('level_spring')
                                               )
        instance.save()
        Coords.objects.create(pereval=instance,
                              latitude=coords_data.get('latitude'),
                              longitude=coords_data.get('longitude'),
                              height=coords_data.get('height')
                               )
        for image_data in images_data:
            PerevalImage.objects.create(pereval=instance,
                                        images=image_data,
                                        title=image_data.name)
        return instance

    def validate(self, data):
        if data['status'] != 'new':
            raise serializers.ValidationError("Статус публикации не 'Новый'")
        return data

    def update(self, instance, validated_data):
        instance.beautyTitle = validated_data['beautyTitle']
        instance.title = validated_data['title']
        instance.other_titles = validated_data['other_titles']
        instance.connect = validated_data['connect']
        instance.level_winter = validated_data['level_winter']
        instance.level_summer = validated_data['level_summer']
        instance.level_autumn = validated_data['level_autumn']
        instance.level_spring = validated_data['level_spring']
        instance.status = validated_data['status']
        instance.save()

        # Удаляем координаты, не включенные в запрос
        latitudes = [item['latitude'] for item in validated_data['coordinates']]
        longitudes = [item['longitude'] for item in validated_data['coordinates']]
        coordinates = instance.coordinates.all()
        for coordinate in coordinates:
            if coordinate.latitude not in latitudes and coordinate.longitude not in longitudes:
                coordinate.delete()

        # Создаем или обновляем новые координаты
        for item in validated_data['coordinates']:
            coordinate = Coords(id=item['id'], latitude=item['latitude'], longitude=item['longitude'],
                                height=item['height'], pereval=instance)
            coordinate.save()

        # Удаляем изображения, не включенные в запрос
        id_image = [item['id'] for item in validated_data['photos']]
        images = instance.photos.all()
        for image in images:
            if image.id not in id_image:
                image.delete()

        # Создаем или обновляем новые изображения
        for item in validated_data['photos']:
            image = PerevalImage(id=item['id'], title=item['title'], pereval=instance)
            image.save()
        return instance
