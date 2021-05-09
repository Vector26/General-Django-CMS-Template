from rest_framework import serializers
from Profile.serializers import FollowProfileSerializer
from .models import *

class PostSerializer(serializers.ModelSerializer):
    profile=FollowProfileSerializer()
    likes=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()
    isLiked=serializers.SerializerMethodField()
    class Meta:
        model=PostContent
        fields="__all__"
    def get_likes(self,obj):
        return obj.getLikes()
    def get_isLiked(self,obj):
        user=self.context.get('request').user
        profile=Profile.objects.get(user=user)
        if(Likes.objects.filter(post=obj, liker=profile).exists()):
            return 1
        else:
            return 0
    def get_comments(self,obj):
        return PostCommentSerializer(obj.getComments(),context=self.context,many=True).data
    def create(self, validated_data):
        p=PostContent.objects.create(
            profile=validated_data['profile'],
            content=validated_data['content']
        )
        p.save()
        return PostSerializer(p).data

    def update(self,instance,validated_data):
        instance.content=validated_data['content']
        instance.save()
        return PostSerializer(instance,context=self.context).data

class LikePostSerializer(serializers.ModelSerializer):
    profile=FollowProfileSerializer()
    likes=serializers.SerializerMethodField()
    comments=serializers.SerializerMethodField()
    # isLiked=serializers.SerializerMethodField()
    class Meta:
        model=PostContent
        fields="__all__"
    def get_likes(self,obj):
        return obj.getLikes()
    # def get_isLiked(self,obj):
        # user=self.context.get('request').user
        # profile=Profile.objects.get(user=user)
        # if(Likes.objects.filter(post=obj, liker=profile).exists()):
        #     return 1
        # else:
        #     return 0
    def get_comments(self,obj):
        return PostCommentSerializer(obj.getComments(),context=self.context,many=True).data
    def create(self, validated_data):
        p=PostContent.objects.create(
            profile=validated_data['profile'],
            content=validated_data['content']
        )
        p.save()
        return PostSerializer(p).data

    def update(self,instance,validated_data):
        instance.content=validated_data['content']
        instance.save()
        return PostSerializer(instance).data

class LikeSerializer(serializers.ModelSerializer):
    post=LikePostSerializer()
    liker=FollowProfileSerializer()
    class Meta:
        model=Likes
        fields="__all__"

    def create(self, validated_data):
        p=Likes.objects.create(
            liker=validated_data['liker'],
            post=validated_data['post']
        )
        p.save()
        return LikeSerializer(p,context=self.context).data

class CommentSerializer(serializers.ModelSerializer):
    commenter=FollowProfileSerializer()
    post=PostSerializer()
    isOwned=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields="__all__"
    def create(self, validated_data):
        p=Comment.objects.create(
            commenter=validated_data['commenter'],
            comment=validated_data['comment'],
            post=validated_data['post']
        )
        p.save()
        return CommentSerializer(p,self.context).data

    def get_isOwned(self,obj):
        user = self.context.get('request').user
        profile = Profile.objects.get(user=user)
        if (Comment.objects.filter(comment=obj,commenter=profile).exists()):
            return 1
        else:
            return 0

    def update(self,instance,validated_data):
        instance.content=validated_data['comment']
        instance.save()
        return CommentSerializer(instance,self.context).data

class PostCommentSerializer(serializers.ModelSerializer):
    commenter=FollowProfileSerializer()
    isOwned=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        exclude=["post"]

    def get_isOwned(self,obj):
        user = self.context.get('request').user
        profile = Profile.objects.get(user=user)
        if (Comment.objects.filter(comment=obj,commenter=profile).exists()):
            return 1
        else:
            return 0
