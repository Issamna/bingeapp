from datetime import date, timedelta
from unittest.mock import patch, Mock, MagicMock
from django.db import IntegrityError
from django.test import TestCase

from api.models.tvshow import Genre, TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User
from .response_data import RESPONSE_DATA


class TestGenreModel(TestCase):
    """Test module for Genre"""

    def setUp(self):
        Genre.objects.create(api_id="1", name="Testery")

    def test_genre_created(self):
        genre = Genre.objects.get(api_id="1")
        self.assertEqual(genre.name, "Testery")

    def test_genre_unique(self):
        with self.assertRaises(Exception):
            Genre.objects.create(api_id="1", name="Testery")


class TestTvShowModel(TestCase):
    """Test module for TvShow model"""

    def setUp(self):
        TvShow.objects.create(
            show_title="TestShow",
            api_id="1",
        )

    def test_tvshow_created(self):
        tvshow = TvShow.objects.get(show_title="TestShow")
        self.assertEqual(tvshow.show_title, "TestShow")
        self.assertFalse(tvshow.is_detailed)

    @patch("requests.get")
    def test_get_show_detail(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_response.json = Mock(return_value=RESPONSE_DATA)
        mock_get.return_value = mock_response

        tvshow = TvShow.objects.get(show_title="TestShow")
        tvshow.get_show_detail()

        self.assertTrue(tvshow.is_detailed)
        self.assertEqual(tvshow.in_production, RESPONSE_DATA.get("in_production"))
        self.assertEqual(tvshow.number_of_episodes, RESPONSE_DATA.get("number_of_episodes"))
        self.assertEqual(tvshow.number_of_seasons, RESPONSE_DATA.get("number_of_seasons"))


class TestUserTvShowModel(TestCase):
    "Test module for UserTvShow model"

    def setUp(self):
        # Test data
        self.email = "test@test.com"
        self.show_title = "TestShow"
        self.user = User.objects.create(
            email=self.email,
            password="12345",
        )
        self.show = TvShow.objects.create(
            show_title=self.show_title,
            api_id="1",
        )
        self.user_tvshow = UserTvShow.objects.create(
            userprofile=self.user.userprofile, show=self.show
        )
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
        )

    def test_usertvshow_created(self):
        usertvshow = UserTvShow.objects.get(
            userprofile=self.user.userprofile, show__show_title=self.show_title
        )
        self.assertEqual(usertvshow.show.show_title, self.show_title)

    def test_create_duplicate(self):
        """Test unique together for duplicates"""
        with self.assertRaises(Exception):
            UserTvShow.objects.create(userprofile=self.user.userprofile, show=self.show)

    def test_last_watched(self):
        self.assertEqual(self.user_tvshow.last_watched, date.today())

    def test_times_watched(self):
        self.assertEqual(self.user_tvshow.times_watched, 1)

    def test_average_watch_length(self):
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow,
            start_date=date.today() + timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        self.user_tvshow.refresh_from_db()
        self.assertEqual(self.user_tvshow.average_watch_length, 2)

    def test_rating_constraint_max(self):
        constraint_name = "api_usertvshow_rating_range"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            self.user_tvshow.rating = 6
            self.user_tvshow.save()

    def test_rating_constraint_min(self):
        constraint_name = "api_usertvshow_rating_range"
        with self.assertRaisesMessage(IntegrityError, constraint_name):
            self.user_tvshow.rating = -1
            self.user_tvshow.save()


class TestViewHistoryModel(TestCase):
    "Test module for ViewHistory Model"

    def setUp(self):
        # Test data
        self.email = "test@test.com"
        self.show_title = "TestShow"
        self.user = User.objects.create(
            email=self.email,
            password="12345",
        )
        self.show = TvShow.objects.create(
            show_title=self.show_title,
            api_id="1",
        )
        self.user_tvshow = UserTvShow.objects.create(
            userprofile=self.user.userprofile, show=self.show
        )
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow, start_date=date.today()
        )

    def test_viewhistory_created(self):
        view_history = ViewHistory.objects.get(user_tvshow=self.user_tvshow)
        self.assertEqual(view_history.user_tvshow, self.user_tvshow)

    def test_watch_length(self):
        """Test viewhistory watch_length property"""
        view_history = ViewHistory.objects.get(user_tvshow=self.user_tvshow)
        self.assertEqual(view_history.watch_length, None)

        view_history.end_date = view_history.start_date + timedelta(days=2)
        view_history.save()
        view_history.refresh_from_db()
        self.assertEqual(view_history.watch_length, 2)
