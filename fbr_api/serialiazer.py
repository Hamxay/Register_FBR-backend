from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import FBR, RegisterUser

class AllFRBSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBR
        fields = '__all__'

class GetUserDetailserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","is_superuser","username","first_name","last_name","email","is_active")

class AddFRBSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBR
        fields = ('title', 'description','location','district',
        'police_station','catagory','mobile_number','is_seen')

class IsSeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBR
        fields = ('is_seen',)

class AddCnicSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ('cnic',)

class RegisterCnic(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = "__all__"

class UserDetail(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ('__all__')

from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user