import requests

from django.db import models

from bingebase.settings import API_KEY
from bingeauth.models.userprofile import UserProfile


class Genre(models.Model):
    """
    Genre for show
    """

    api_id = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = [["api_id", "name"]]


class TvShow(models.Model):
    """
    TV show model
    """

    # created
    show_title = models.CharField(max_length=255, null=False)
    api_id = models.CharField(default=None, max_length=255, null=False)
    is_detailed = models.BooleanField(default=False)
    first_air_date = models.DateField(
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(Genre)
    vote_average = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    vote_count = models.IntegerField(null=True)
    overview = models.TextField(null=True)
    poster_path = models.CharField(max_length=255, null=True)
    # filled after get_show_detail
    in_production = models.BooleanField(null=True)
    number_of_episodes = models.IntegerField(null=True)
    number_of_seasons = models.IntegerField(null=True)

    def get_show_detail(self):
        if not self.is_detailed:
            url = "https://api.themoviedb.org/3/tv/{}?api_key={}&language=en-US".format(
                self.api_id, API_KEY
            )
            response = requests.get(url)
            response_data = response.json()
            self.in_production = response_data.get("in_production")
            self.number_of_episodes = response_data.get("number_of_episodes")
            self.number_of_seasons = response_data.get("number_of_seasons")
            #make is detailed true so it will not call again
            self.is_detailed = True
            self.save()


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
    rating = models.IntegerField(null=True)

    @property
    def last_watched(self):
        latest_view_history = self.view_histories.latest("start_date")
        return latest_view_history.start_date

    @property
    def times_watched(self):
        return self.view_histories.count()

    @property
    def average_watch_length(self):
        all_view_history = self.view_histories.filter(end_date__isnull=False)
        total_view_days = sum(
            view_history.watch_length for view_history in all_view_history
        )
        if total_view_days == 0:
            return None
        else:
            return total_view_days / all_view_history.count()

    class Meta:
        unique_together = [["userprofile", "show"]]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_rating_range",
                check=models.Q(rating__range=(0, 5)),
            ),
        ]


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
    start_date = models.DateField(null=False)
    end_date = models.DateField(
        null=True,
        blank=True,
    )

    @property
    def watch_length(self):
        "Returns the view history watch length"
        if self.end_date:
            return (self.end_date - self.start_date).days
        else:
            return None

    class Meta:
        ordering = ["start_date"]
