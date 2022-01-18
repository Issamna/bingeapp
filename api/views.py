from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework import viewsets

from api.models.tvshow import TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User
from api.serializers.tvshows_serializer import (
    TvShowSerializer,
    UserTvShowSerializer,
    ViewHistorySerializer,
)


class TvShowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View set for Tv Show for list and retrieve
    """

    queryset = TvShow.objects.all()
    serializer_class = TvShowSerializer


class UserTvShowViewSet(viewsets.ModelViewSet):
    """
    View set for User Tv Shows
    """

    model = UserTvShow
    serializer_class = UserTvShowSerializer

    #only return users data
    def get_queryset(self):
        user = self.request.user
        return UserTvShow.objects.filter(userprofile=user.userprofile)


class ViewHistoryViewSet(viewsets.ModelViewSet):
    """
    View set for View History
    """

    model = ViewHistory
    serializer_class = ViewHistorySerializer

    #only return users data
    def get_queryset(self):
        user = self.request.user
        return ViewHistory.objects.filter(user_tvshow__userprofile=user.userprofile)
