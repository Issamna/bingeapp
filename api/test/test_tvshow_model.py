from datetime import datetime, timedelta
from django.test import TestCase
from django.utils.timezone import make_aware

from api.models.tvshow import TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User


class TestTvShowModel(TestCase):
    """Test module for TvShow model"""

    def setUp(self):
        TvShow.objects.create(show_title="TestShow")

    def test_tvshow_created(self):
        tvshow = TvShow.objects.get(show_title="TestShow")
        self.assertEqual(tvshow.get_show_info(), "TestShow")


class TestUserTvShowModel(TestCase):
    "Test module for UserTvShow model"

    def setUp(self):
        #Test data
        self.email = "test@test.com"
        self.show_title = "TestShow"
        self.user = User.objects.create(
            email=self.email,
            password="12345",
        )
        self.show = TvShow.objects.create(
            show_title=self.show_title,
        )
        UserTvShow.objects.create(userprofile=self.user.userprofile, show=self.show)

    def test_usertvshow_created(self):
        usertvshow = UserTvShow.objects.get(
            userprofile=self.user.userprofile, show__show_title=self.show_title
        )
        self.assertEqual(usertvshow.show.get_show_info(), self.show_title)

    def test_create_duplicate(self):
        """Test unique together for duplicates"""
        with self.assertRaises(Exception):
            UserTvShow.objects.create(userprofile=self.user.userprofile, show=self.show)


class TestViewHistoryModel(TestCase):
    "Test module for ViewHistory Model"

    def setUp(self):
        #Test data
        self.email = "test@test.com"
        self.show_title = "TestShow"
        self.user = User.objects.create(
            email=self.email,
            password="12345",
        )
        self.show = TvShow.objects.create(
            show_title=self.show_title,
        )
        self.user_tvshow = UserTvShow.objects.create(
            userprofile=self.user.userprofile, show=self.show
        )
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow, start_date=make_aware(datetime.now())
        )

    def test_viewhistory_created(self):
        view_history = ViewHistory.objects.get(user_tvshow=self.user_tvshow)
        self.assertEqual(view_history.user_tvshow, self.user_tvshow)

    def test_watch_length(self):
        """Test viewhistory watch_length property"""
        view_history = ViewHistory.objects.get(user_tvshow=self.user_tvshow)
        self.assertEqual(view_history.watch_length, None)

        view_history.end_date = make_aware(datetime.now() + timedelta(hours=10))
        view_history.save()
        view_history.refresh_from_db()
        self.assertEqual(
            view_history.watch_length, view_history.end_date - view_history.start_date
        )
