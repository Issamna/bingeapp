from rest_framework import serializers
from api.models.tvshow import TvShow, UserTvShow, ViewHistory


class TvShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvShow
        fields = "__all__"


class UserTvShowSerializer(serializers.ModelSerializer):

    last_watched = serializers.ReadOnlyField()

    times_watched = serializers.ReadOnlyField()

    average_watch_length = serializers.ReadOnlyField()

    class Meta:
        model = UserTvShow
        fields = "__all__"


class ViewHistorySerializer(serializers.ModelSerializer):

    watch_length = serializers.ReadOnlyField()

    class Meta:
        model = ViewHistory
        fields = "__all__"
