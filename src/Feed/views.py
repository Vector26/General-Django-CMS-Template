from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
# Create your views here.

class Feed(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = PostSerializer
    def get(self,request):
        if(request.query_params.get('id')):
            if(PostContent.objects.filter(id=request.query_params.get('id')).exists()):
                queryset = PostContent.objects.get(id=request.query_params.get('id'))
                t = PostSerializer(queryset)
            else:
                return Response({"Message":"Post Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            queryset = PostContent.objects.all()
            t=PostSerializer(queryset,many=True)
        return Response(t.data,status=status.HTTP_200_OK)
    def post(self,request):
        profile = Profile.objects.get(user=request.user)
        if (request.data.get('id')):
            if (PostContent.objects.filter(id=request.data.get('id'),profile=profile).exists()):
                # Update a post
                inst=PostContent.objects.get(profile=profile,id=request.data.get('id'))
                t=PostSerializer()
                data=t.update(instance=inst,validated_data={"content":request.data.get('content')})
                return Response({"Data":data},status=status.HTTP_200_OK)
            else:
                return Response({"Message": "Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            t=PostSerializer()
            t=t.create({"profile":profile,"content":request.data.get('content')})
        return Response(t, status=status.HTTP_200_OK)

    def delete(self,request):
        profile = Profile.objects.get(user=request.user)
        if (request.data.get('id')):
            if (PostContent.objects.filter(id=request.data.get('id'), profile=profile).exists()):
                # Update a post
                PostContent.objects.get(id=request.data.get('id'), profile=profile).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Message": "Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Message": "Insufficient Variables Provided"}, status=status.HTTP_400_BAD_REQUEST)

class Likesview(APIView):
    def post(self,request):
        profile = Profile.objects.get(user=request.user)
        if (request.data.get('id')):
            if (PostContent.objects.filter(id=request.data.get('id')).exists()):
                # Update a post
                inst = PostContent.objects.get(id=request.data.get('id'))
                if (Likes.objects.filter(liker=profile,post=inst).exists()):
                    Likes.objects.get(liker=profile, post=inst).delete()
                    return Response({"Message":"Disliked"},status=status.HTTP_204_NO_CONTENT)
                else:
                    t = LikeSerializer()
                    data = t.create({"liker": profile, "post":inst})
                return Response({"Message":"Liked","Data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Message":"Insufficient Data"}, status=status.HTTP_400_BAD_REQUEST)

class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    # serializer_class = PostSerializer
    def get(self,request):
        if(request.query_params.get('id')):
            if(Comment.objects.filter(id=request.query_params.get('id')).exists()):
                queryset = Comment.objects.get(id=request.query_params.get('id'))
                t = CommentSerializer(queryset)
            else:
                return Response({"Message":"Post Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        elif(request.query_params.get('post_id')):
            if(PostContent.objects.filter(id=request.query_params.get('post_id')).exists()):
                post=PostContent.objects.get(id=request.query_params.get('post_id'))
            else:
                return Response({"message":"Post not found"},status=status.HTTP_400_BAD_REQUEST)
            queryset = Comment.objects.filter(post=post)
            t=PostCommentSerializer(queryset,many=True)
        return Response(t.data,status=status.HTTP_200_OK)
    def post(self,request):
        profile = Profile.objects.get(user=request.user)
        if (request.data.get('post_id') and request.data.get('comment')):
            if (PostContent.objects.filter(id=request.data.get('post_id')).exists()):
                # Update a post
                inst=PostContent.objects.get(id=request.data.get('post_id'))
                t=CommentSerializer()
                data=t.create(validated_data={"comment":request.data.get('comment'),"commenter":profile,"post":inst})
                return Response({"Data":data},status=status.HTTP_200_OK)
            else:
                return Response({"Message": "Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        profile=Profile.objects.get(user=request.user)
        if(request.data.get('post_id') and request.data.get('id')):
            if(PostContent.objects.filter(id=request.data.get('post_id')).exists()):
                post=PostContent.objects.get(id=request.data.get('post_id'))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if(Comment.objects.filter(post=post,commenter=profile,id=request.data.get('id')).exists()):
                Comment.objects.get(post=post, commenter=profile, id=request.data.get('id')).delete()
                return Response({"Message":"Comment Deleted"},status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
