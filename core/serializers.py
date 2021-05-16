import re

from rest_framework import serializers

from .models import User, GlobalDatabase

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name','phone','password','email']
        extra_kwargs = {
            'name': {'required': True},
            'phone': {'required': True}
        }

    def validate_phone(self,value):
        
        p = re.compile("(0/91)?[7-9][0-9]{9}")

        if p.match(value):
            return value
        else:
            raise serializers.ValidationError('Wrong input for phone')

    
    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data['phone'],
            name=validated_data['name'],
            email=validated_data.get('email')
        )

        user.set_password(validated_data['password'])
        user.save()

        # Adding the registered user to the global database
        GlobalDatabase.objects.create(
            name = validated_data.get('name'),
            phone = validated_data.get('phone'),
            email = validated_data.get('email'),
            registration_status = True,
            user = user
        )

        return user


class GlobalDatabaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GlobalDatabase
        fields = ['name','phone','spam_status']