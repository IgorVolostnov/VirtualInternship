from rest_framework.exceptions import ValidationError
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
        print(validated_data)
        user_data = validated_data.pop('user')
        try:
            user = User.objects.get(email=user_data.get('email'))
        except User.DoesNotExist:
            user = User.objects.create(**user_data)
        instance = Author.objects.create(user=user, **validated_data)
        instance.save()
        return instance

    def validate(self, data):
        if self.instance:  # 'instance' will be set in case of `PUT` request i.e update
            object_id = self.instance.id  # get the 'id' for the instance
            # write your validation logic based on the object id here
            print(object_id)
        print(data)
        return data


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImage
        fields = ('id', 'title', 'images')


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
                                        image=image_data,
                                        title=image_data.name)
        return instance

    def validate(self, data):
        if self.instance:  # 'instance' will be set in case of `PUT` request i.e update
            object_id = self.instance.id  # get the 'id' for the instance
            # write your validation logic based on the object id here
            print(object_id)
        print(data)
        return data
