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
        fields = ('title', 'description')

class RegisterCnic(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password', 'password2',
                  )

    def save(self):
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        # if User.objects.filter(email__iexact=email).exists():
        #     raise serializers.ValidationError(
        #         {"Email": "Email Already Exist."})
        account.set_password(password)
        account.save()
        return account