from django.db import models

from bingeauth.models.userprofile import UserProfile


class TvShow(models.Model):
    """
    TV show model
    """
    show_title = models.CharField(
        max_length=255,
        null=False
    )

    def get_show_info(self):
        return self.show_title

    def __str__(self):
        return self.show_title


class UserTvShow(models.Model):
    """
    User's tvshows
    """
    user_profile = models.ForeignKey(
        UserProfile,
        related_name="user_shows",
        on_delete=models.CASCADE,
        null=False,
    )
    show = models.ForeignKey(
        TvShow,
        related_name="show_users",
        on_delete=models.CASCADE,
        null=False
    )
    last_watched = models.DateTimeField()
    times_watched = models.IntegerField(default=0)

    def __str__(self):
        return show.show_title + ' watched by ' + user_profile.username
    