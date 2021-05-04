from django.urls import path,include
from .views import *
urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('',ProfileInfo.as_view(),name="getProfile"),
    path('signUp',Signup.as_view(),name="signUp"),
    path('search',SearchAPI.as_view(),name="searchAPI"),
    path('follow',FollowView.as_view(),name="follow"),
    path('Feed', include('Feed.urls')),
]