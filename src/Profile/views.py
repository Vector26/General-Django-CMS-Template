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

class ProfileInfo(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        flag=True
        if(not request.query_params.get('id')):
            profile=Profile.objects.get(user=request.user)
        else:
            id=request.query_params.get('id')
            if(Profile.objects.filter(id=id).exists()):
                profile=Profile.objects.get(id=id)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            profileO = Profile.objects.get(user=request.user)
            if(FollowerSystem.objects.filter(FollowedUser=profile,Follower=profileO).exists()):
                flag=True
            else:
                flag=False
        s1 = ProfileSerializer(profile, many=False)
        data={}
        data["Profile"]=s1.data
        if(flag):
            Followers = FollowerSystem.objects.filter(FollowedUser=profile)
            Followed = FollowerSystem.objects.filter(Follower=profile)
            s2 = FollowersSerializer(Followers, many=True)
            data["Followers"]=s2.data
            s3 = FollowedSerializer(Followed, many=True)
            data["Followed"] = s3.data
        return Response(data, status=status.HTTP_200_OK)

    def post(self,request):
        u=UserSerializer(instance=request.user)
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
            if(request.data.get("action")==0):
                data = {"FollowedUser": followedAuthor, "Follower": author}
                serializer = FollowSerializer()
                vD=serializer.create(validated_data=data)
                sR=FollowSerializer(vD)
                return Response({"Message":"Followed","Detail":sR.data}, status=status.HTTP_201_CREATED)
            elif(request.data.get("action")==1):
                followRelation = FollowerSystem.objects.get(FollowedUser=followedAuthor, Follower=author)
                followRelation.delete()
                return Response({"Message":"Unfollowed"},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Message":"Unusual activity reported"},status=status.HTTP_400_BAD_REQUEST)
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