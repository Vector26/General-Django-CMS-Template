from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import *
from Feed.models import PostContent
import base64
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=["password","is_superuser","is_staff","is_active","groups","user_permissions"]

    def decodeDesignImage(self,data):
        try:
            data=str(data).replace("data:image/png;base64,","")
            data=str(data).replace(" ","+")
            data = base64.b64decode(data.encode('UTF-8'))
            buf = io.BytesIO(data)
            img = Image.open(buf)
            return img
        except:
            return None

    def update(self, instance, validated_data):
        try:
            img = self.decodeDesignImage(validated_data.get('profile_pic'))
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            instance.ProfileUser.image = InMemoryUploadedFile(img_io, field_name=None,name=instance.first_name + "ProfilePic.jpeg",content_type='image/jpeg', size=img_io.tell, charset=None)
        except:
            print("Exception")
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.ProfileUser.Bio = validated_data.get('bio', instance.ProfileUser.Bio)
        # instance.ProfileUser.image = validated_data.get('profile_pic', instance.ProfileUser.image)
        return instance

class Register(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2=serializers.CharField(write_only=True,required=True)

    class Meta:
        model=User
        fields=('username','password','password2','email','first_name','last_name')
        extra_kwargs={
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    FRC=serializers.SerializerMethodField()
    FDC=serializers.SerializerMethodField()
    PC=serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields="__all__"
    def get_FDC(self,obj):
        return obj.getFollowedCount()
    def get_FRC(self,obj):
        return obj.getFollowersCount()
    def get_PC(self,obj):
        return PostContent.objects.filter(profile=obj).count()

# Search Serializers__________________________

class SearchProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=["Bio","image"]

class SearchUserSerializer(serializers.ModelSerializer):
    ProfileUser=SearchProfileSerializer()
    class Meta:
        model=User
        fields = ["username", "first_name", "last_name", "email", "id","ProfileUser"]
# Follow Serializers___________________________

class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","id"]

class FollowProfileSerializer(serializers.ModelSerializer):
    user=FollowUserSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=["user","Bio","id","image"]

class FollowersSerializer(serializers.ModelSerializer):
    Follower=FollowProfileSerializer(read_only=True)
    class Meta:
        model=FollowerSystem
        exclude=["FollowedUser","id"]

class FollowedSerializer(serializers.ModelSerializer):
    FollowedUser=FollowProfileSerializer(read_only=True)
    class Meta:
        model=FollowerSystem
        exclude=["Follower","id"]

class FollowSerializer(serializers.ModelSerializer):
    FollowedUser=FollowProfileSerializer(read_only=True)
    Follower=FollowProfileSerializer(read_only=True)
    class Meta:
        model=FollowerSystem
        exclude=["id"]

    def create(self, validated_data):
        FA = validated_data.get('FollowedUser')
        A = validated_data.get('Follower')
        serializer = FollowerSystem.objects.create(FollowedUser=FA, Follower=A)
        #                 # if serializer.is_valid():
        serializer.save()
        return serializer
