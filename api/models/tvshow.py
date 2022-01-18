from django.db import models

from bingeauth.models.userprofile import UserProfile


class TvShow(models.Model):
    """
    TV show model
    """

    show_title = models.CharField(max_length=255, null=False)

    def get_show_info(self):
        return self.show_title


class UserTvShow(models.Model):
    """
    User's tvshows
    """

    userprofile = models.ForeignKey(
        UserProfile,
        related_name="user_shows",
        on_delete=models.CASCADE,
        null=False,
    )
    show = models.ForeignKey(
        TvShow, related_name="show_users", on_delete=models.CASCADE, null=False
    )

    last_watched = models.DateTimeField(
        null=True,
        blank=True,
    )
    times_watched = models.IntegerField(default=0)

    class Meta:
        unique_together = [["userprofile", "show"]]


class ViewHistory(models.Model):
    """
    Users view history for the tv show
    """

    user_tvshow = models.ForeignKey(
        UserTvShow,
        related_name="view_histories",
        on_delete=models.CASCADE,
        null=False,
    )
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    @property
    def watch_length(self):
        "Returns the view history watch length"
        if self.end_date:
            return self.end_date - self.start_date
        else:
            return None
