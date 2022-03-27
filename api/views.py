import json
from django.http import JsonResponse
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets

from api.models.tvshow import TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User
from api.serializers.tvshows_serializer import (
    TvShowSerializer,
    UserTvShowSerializer,
    ViewHistorySerializer,
)
from bingeauth.models.userprofile import UserProfile


class TvShowViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View set for Tv Show for list and retrieve
    """

    queryset = TvShow.objects.all()
    serializer_class = TvShowSerializer

    @action(detail=False, methods=["GET"], name="searchtvshow")
    def search_tv_show(self, request, pk=None):
        search_term = request.query_params.get("search")
        tv_shows = TvShow.objects.filter(show_title__icontains=search_term)
        serializer = TvShowSerializer(tv_shows, many=True)
        return Response(serializer.data)


class UserTvShowViewSet(viewsets.ModelViewSet):
    """
    View set for User Tv Shows
    """

    model = UserTvShow
    serializer_class = UserTvShowSerializer

    def create(self, request):
        # update show details
        if not request.data.get("userprofile"):
            request.data.update(
                {"userprofile": UserProfile.objects.get(user=request.user).pk}
            )
        tvshow_id = request.data.get("show")
        try:
            tvshow = TvShow.objects.get(pk=tvshow_id)
            tvshow.get_show_detail()
        except TvShow.DoesNotExist:
            # TODO: Log error
            print("error TvShow.DoesNotExist")
        except APIException:
            print("A server error occurred. Failed to retrieve show details")
        except Exception as e:
            print(e)

        return super().create(request)

    # only return users data
    def get_queryset(self):
        user = self.request.user
        return UserTvShow.objects.filter(userprofile=user.userprofile)

    @action(detail=True, methods=["GET"], name="allviewhistory")
    def all_view_history(self, request, pk=None):
        # returns user tvshow view history
        user = request.user
        view_histories = UserTvShow.objects.get(
            userprofile=user.userprofile,
            pk=pk,
        ).view_histories.all()
        serializer = ViewHistorySerializer(view_histories, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=["GET"], name="getusershows")
    def get_user_shows(self, request, pk=None):
        user = self.request.user
        tv_shows_ids = (
            UserTvShow.objects.filter(userprofile=user.userprofile)
            .values_list("show__pk", flat=True)
            .distinct()
        )
        tv_shows = TvShow.objects.filter(pk__in=tv_shows_ids)
        serializer = TvShowSerializer(tv_shows, many=True)
        return Response(serializer.data)


class ViewHistoryViewSet(viewsets.ModelViewSet):
    """
    View set for View History
    """

    model = ViewHistory
    serializer_class = ViewHistorySerializer

    # only return users data and only for usertvshow
    def get_queryset(self):
        user = self.request.user
        return ViewHistory.objects.filter(
            user_tvshow__userprofile=user.userprofile,
        )
