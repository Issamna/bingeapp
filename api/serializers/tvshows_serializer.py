from rest_framework import serializers
from api.models.tvshow import TvShow, UserTvShow, ViewHistory


class TvShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvShow
        fields = "__all__"


class UserTvShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTvShow
        fields = "__all__"


class ViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewHistory
        fields = "__all__"
