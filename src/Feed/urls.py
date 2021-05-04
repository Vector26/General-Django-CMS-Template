from django.urls import path
from .views import *
urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('',Feed.as_view(),name="getFeed"),
    path('/like',Likesview.as_view(),name="Like"),
    path('/comment',CommentView.as_view(),name="Comment"),
            ]