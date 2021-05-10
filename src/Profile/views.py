from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from Feed.serializers import PostSerializer
# Create your views here.

class ProfileInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        isItself=0
        flag=True
        if(not request.query_params.get('id')):
            profile=Profile.objects.get(user=request.user)
            isItself=1
        else:
            id=request.query_params.get('id')
            if(Profile.objects.filter(id=id).exists()):
                profile=Profile.objects.get(id=id)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            profileO = Profile.objects.get(user=request.user)
            if (profile.user.username == profileO.user.username and profile.user.password==profileO.user.password):
                isItself=1
            if(FollowerSystem.objects.filter(FollowedUser=profile,Follower=profileO).exists()):
                flag=True
            else:
                flag=False
        s1 = ProfileSerializer(profile, many=False)
        data={}
        data["isItself"] = isItself
        data["Profile"]=s1.data
        if(flag or isItself==1):
            Posts=PostSerializer(PostContent.objects.filter(profile=profile),many=True,context={"request":request}).data
            data["Posts"]=Posts
        return Response(data, status=status.HTTP_200_OK)

    def post(self,request):
        u=UserSerializer(instance=request.user)
        print(request.POST)
        t=u.update(instance=request.user,validated_data=request.data)
        t.save()
        p=Profile.objects.get(user=t)
        data=ProfileSerializer(p).data
        return Response({"User":data},status=status.HTTP_200_OK)

# class Signup(APIView):
#     permission_classes = (AllowAny,)
#     def post(self,request):
#         u=Register(data=request.data)
#         t=Register(u.create(u.validate(request.data)))
#         if u:
#             return Response({"user":t.data},status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = Register

# class ProfileView(APIView):
#     def get(self, request):
#         author=Author.objects.get(user=request.user)
#         serializer4=AuthorSerializer(author,many=False)
#         return Response({"author":serializer4.data})

class FollowView(APIView):
    def get(self, request):
        author = Profile.objects.get(user=request.user)
        if(request.query_params.get('id')):
            if (User.objects.filter(id=request.query_params.get('id')).exists()):
                temp=User.objects.get(id=request.query_params.get('id'))
                profile=Profile.objects.get(user=temp)
                if(FollowerSystem.objects.filter(FollowedUser=temp,Follower=author).exists()):
                    author=temp
                else:
                    return Response({"Message":"Not allowed"},statusstatus.HTTP_403_FORBIDDEN)
        follower = FollowerSystem.objects.filter(FollowedUser=author)
        followed = FollowerSystem.objects.filter(Follower=author)
        serializer2 = FollowersSerializer(follower, many=True)
        serializer3=FollowedSerializer(followed,many=True)
        return Response({"followers": serializer2.data,"followings":serializer3. data})

    def post(self, request):
        if(User.objects.filter(id=request.data.get('id')).exists()):
            user=User.objects.get(id=request.data.get('id'))
            followedAuthor = Profile.objects.get(user=user)
            author = Profile.objects.get(user=request.user)
            if(not FollowerSystem.objects.filter(FollowedUser=followedAuthor,Follower=author).exists()):
                data = {"FollowedUser": followedAuthor, "Follower": author}
                serializer = FollowSerializer()
                vD=serializer.create(validated_data=data)
                sR=FollowSerializer(vD)
                return Response({"Message":"Followed","Detail":sR.data}, status=status.HTTP_201_CREATED)
            else:
                followRelation = FollowerSystem.objects.get(FollowedUser=followedAuthor, Follower=author)
                followRelation.delete()
                return Response({"Message":"Unfollowed"},status=status.HTTP_200_OK)
        else:
            return Response({"Message":"User does not exist"},status=status.HTTP_404_NOT_FOUND)

class SearchAPI(APIView):
    def get(self,request):
        # print(request.query_params.get('h'))
        if(request.query_params.get('username')):
            name=request.query_params.get('username')
            QS=User.objects.filter(username__contains=name)
            ser=SearchUserSerializer(QS,many=True)
            # ser2=FollowProfileSerializer(QS,many=True)
            return Response({"data":ser.data},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)