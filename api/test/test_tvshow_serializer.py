from datetime import date, timedelta
from unittest.mock import patch, Mock, MagicMock
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import make_aware

from api.models.tvshow import TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User
from .response_data import RESPONSE_DATA

client = APIClient()


class TestTvShowSerializer(TestCase):
    """Test module for TvShow Serializer/View"""

    def setUp(self):
        # Test data
        self.show = TvShow.objects.create(show_title="TestShow", api_id="1")
        TvShow.objects.create(show_title="TestShow2", api_id="2")
        self.owner = User.objects.create(
            email="test@test.com",
        )
        client.force_authenticate(user=self.owner)

    def test_list(self):
        response = client.get(reverse("tvshows-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve(self):
        find_show = TvShow.objects.get(show_title="TestShow2")
        response = client.get(reverse("tvshows-detail", args=[find_show.pk]))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["show_title"], "TestShow2")

    def test_retrieve_not_exist(self):
        response = client.get(reverse("tvshows-detail", args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_other_calls(self):
        """ "Test to make sure only list and retrieve work"""
        payload = {
            "show_title": "New_Title",
        }
        response_create = client.post(reverse("tvshows-list"), payload)
        response_update = client.put(
            reverse("tvshows-detail", args=[self.show.pk]), payload
        )
        response_delete = client.delete(reverse("tvshows-detail", args=[self.show.pk]))
        self.assertEqual(response_create.status_code, 405)
        self.assertEqual(response_update.status_code, 405)
        self.assertEqual(response_delete.status_code, 405)


class TestUserTvShowSerializer(TestCase):
    """Test module for UserTvShow Serializer/View"""

    def setUp(self):
        # Test data
        self.show1 = TvShow.objects.create(show_title="TestShow1", api_id="1")
        self.show2 = TvShow.objects.create(show_title="TestShow2", api_id="2")
        self.show3 = TvShow.objects.create(show_title="TestShow3", api_id="3")
        self.owner = User.objects.create(email="test@test.com")
        self.user_tvshow1 = UserTvShow.objects.create(
            userprofile=self.owner.userprofile, show=self.show1
        )
        self.user_tvshow2 = UserTvShow.objects.create(
            userprofile=self.owner.userprofile, show=self.show2
        )
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow1,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )
        ViewHistory.objects.create(
            user_tvshow=self.user_tvshow2,
            start_date=date.today(),
        )
        # Different user to test list/retrieve only user data
        self.diff_user = User.objects.create(email="diff_user@test.com")
        UserTvShow.objects.create(
            userprofile=self.diff_user.userprofile, show=self.show2
        )
        client.force_authenticate(user=self.owner)

    def test_list(self):
        response = client.get(reverse("utvshows-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve(self):
        response = client.get(reverse("utvshows-detail", args=[self.user_tvshow1.pk]))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["show"], 1)

    def test_all_view_history(self):
        response = client.get(
            reverse("utvshows-all-view-history", args=[self.user_tvshow1.pk])
        )
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)

    def test_properties(self):
        response = client.get(reverse("utvshows-detail", args=[self.user_tvshow1.pk]))
        response_data = response.json()
        self.assertEqual(response_data["last_watched"], str(date.today()))
        self.assertEqual(response_data["times_watched"], 1)
        self.assertEqual(response_data["average_watch_length"], 1.0)

    def test_retrieve_bad_data(self):
        # to test if it does not exist
        response = client.get(reverse("utvshows-detail", args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_create_no_up(self):
        payload = {"show": self.show3.pk}
        response = client.post(reverse("utvshows-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show3
            ).exists()
        )

    def test_create(self):
        payload = {"userprofile": self.owner.userprofile.pk, "show": self.show3.pk}
        response = client.post(reverse("utvshows-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show3
            ).exists()
        )

    @patch("requests.get")
    def test_create_updates_show_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_response.json = Mock(return_value=RESPONSE_DATA)
        mock_get.return_value = mock_response
        self.assertFalse(self.show3.is_detailed)
        payload = {"userprofile": self.owner.userprofile.pk, "show": self.show3.pk}
        response = client.post(reverse("utvshows-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show3
            ).exists()
        )
        self.show3.refresh_from_db()
        self.assertTrue(self.show3.is_detailed)
        self.assertEqual(self.show3.in_production, RESPONSE_DATA.get("in_production"))
        self.assertEqual(self.show3.number_of_episodes, RESPONSE_DATA.get("number_of_episodes"))
        self.assertEqual(self.show3.number_of_seasons, RESPONSE_DATA.get("number_of_seasons"))

    @patch("requests.get")
    def test_create_updates_show_details_fails(self, mock_get):
        # fail api response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json = Mock(return_value=None)
        mock_get.return_value = mock_response

        payload = {"userprofile": self.owner.userprofile.pk, "show": self.show3.pk}
        response = client.post(reverse("utvshows-list"), payload)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.data.get("detail"),
            "A server error occurred. Failed to retrieve show details",
        )
        self.assertFalse(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show3
            ).exists()
        )
        self.show3.refresh_from_db()
        self.assertFalse(self.show3.is_detailed)
        self.assertEqual(self.show3.in_production, None)
        self.assertEqual(self.show3.number_of_episodes, None)
        self.assertEqual(self.show3.number_of_seasons, None)

    def test_create_bad_data(self):
        payload = {"userprofile": self.owner.userprofile.pk, "show": 20}
        response = client.post(reverse("utvshows-list"), payload)
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate(self):
        # test unique together on model
        payload = {"userprofile": self.owner.userprofile.pk, "show": self.show1.pk}
        response = client.post(reverse("utvshows-list"), payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show1
            ).count(),
            1,
        )

    def test_update(self):
        payload = {
            "userprofile": self.user_tvshow1.userprofile.pk,
            "show": self.user_tvshow1.show.pk,
            "rating": 5,
        }
        response = client.put(
            reverse("utvshows-detail", args=[self.user_tvshow1.pk]), payload
        )
        self.assertEqual(response.status_code, 200)
        self.user_tvshow1.refresh_from_db()
        self.assertEqual(self.user_tvshow1.rating, 5)

    def test_delete(self):
        response = client.delete(
            reverse("utvshows-detail", args=[self.user_tvshow1.pk])
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            UserTvShow.objects.filter(
                userprofile=self.owner.userprofile, show=self.show1
            ).exists()
        )


class TestViewHistorySerializer(TestCase):
    """Test module for UserTvShow Serializer/View"""

    def setUp(self):
        # Test data
        self.show1 = TvShow.objects.create(show_title="TestShow1", api_id="1")
        self.owner = User.objects.create(email="test@test.com")
        self.user_tvshow = UserTvShow.objects.create(
            userprofile=self.owner.userprofile, show=self.show1
        )
        self.viewhistory1 = ViewHistory.objects.create(
            user_tvshow=self.user_tvshow,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
        )
        self.viewhistory2 = ViewHistory.objects.create(
            user_tvshow=self.user_tvshow,
            start_date=date.today(),
        )

        # Different user to test list/retrieve only user data
        self.diff_user = User.objects.create(email="diff_user@test.com")
        self.diff_user_tvshow = UserTvShow.objects.create(
            userprofile=self.diff_user.userprofile, show=self.show1
        )
        ViewHistory.objects.create(
            user_tvshow=self.diff_user_tvshow, start_date=date.today()
        )
        client.force_authenticate(user=self.owner)

    def test_list(self):
        response = client.get(reverse("viewhistory-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_retrieve(self):
        response = client.get(
            reverse("viewhistory-detail", args=[self.viewhistory1.pk])
        )
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["user_tvshow"], self.viewhistory1.user_tvshow.pk)

    def test_properties(self):
        response = client.get(
            reverse("viewhistory-detail", args=[self.viewhistory1.pk])
        )
        response_data = response.json()
        self.assertEqual(response_data["watch_length"], 1)

    def test_retrieve_bad_data(self):
        # to test if it does not exist
        response = client.get(reverse("viewhistory-detail", args=[10]))
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        payload = {"user_tvshow": self.user_tvshow.pk, "start_date": date.today()}
        response = client.post(reverse("viewhistory-list"), payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ViewHistory.objects.filter(pk=self.viewhistory1.pk).exists())

    def test_update(self):
        end_date = date.today() + timedelta(days=4)
        payload = {
            "user_tvshow": self.viewhistory2.pk,
            "start_date": self.viewhistory2.start_date,
            "end_date": end_date,
        }
        response = client.put(
            reverse("viewhistory-detail", args=[self.viewhistory2.pk]), payload
        )
        self.assertEqual(response.status_code, 200)
        self.viewhistory2.refresh_from_db()
        self.assertEqual(self.viewhistory2.end_date, end_date)

    def test_delete(self):
        response = client.delete(
            reverse("viewhistory-detail", args=[self.viewhistory1.pk])
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(ViewHistory.objects.filter(pk=self.viewhistory1.pk).exists())
