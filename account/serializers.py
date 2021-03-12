# restframework imports
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
#jwt
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
# djnago imports
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
#utils
from utils import res_codes

# in house apps import
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    country = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)
    organization = serializers.CharField(required=True)
    
    class Meta:
        model = Profile
        fields = [
            'country',
            'date_of_birth',
            'organization',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [
            UniqueValidator(queryset=User.objects.all())
            ]
        )
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'profile', 
        ]
        extra_kwargs = {
            'password': {'write_only': True,},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user_obj = User.objects.create(**validated_data)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        profile = user_obj.profile
        profile_serializer = ProfileSerializer(
            profile,
            data = profile_data
            )
        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            raise serializers.ValidationError(
                profile_serializer.errors
                )
        return user_obj

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        Profile.objects.filter(user=instance).update(**profile_data)
        User.objects.filter(id=instance.id).update(**validated_data)
        user = User.objects.get(id=instance.id)
        return user




class SubscriberAuthSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # if self.user.profile.role != 1:
        #     raise serializers.ValidationError(
        #         res_codes.get_response_dict(
        #             res_codes.NO_ACCESS
        #         )
        #     )

        return data


class InstructorAuthSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.profile.role != 2:
            raise serializers.ValidationError(
                res_codes.get_response_dict(
                    res_codes.NO_ACCESS
                )
            )

        return data


class AdminAuthSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.profile.role != 3:
            raise serializers.ValidationError(
                res_codes.get_response_dict(
                    res_codes.NO_ACCESS
                )
            )

        return data


class ProfileDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'country',
            'date_of_birth',
            'organization',
            'mobile',
            'address',
            'city',
            'pincode',
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileDetailSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'profile',
        ]


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = [
            'password',
            'new_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True,},
        }

    def validate_password(self, data):
        if not check_password(data, self.instance.password):
            raise serializers.ValidationError(
                    res_codes.get_response_dict(
                        res_codes.WRONG_PASSWORD_ENTERED
                    )
                )
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance