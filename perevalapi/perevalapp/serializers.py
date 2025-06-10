from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Author
        fields = ['id', 'fam', 'name', 'otc', 'user', 'phone']

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        print(user_data)
        try:
            user = User.objects.get(email=user_data.get('email'))
        except User.DoesNotExist:
            user = User.objects.create(**user_data)
        instance = Author.objects.create(user=user, **validated_data)
        instance.save()
        return instance