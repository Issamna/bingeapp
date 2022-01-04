from django.test import TestCase
from api.models.tvshow import TvShow


class TestTvShow(TestCase):
    """ Test module for TvShow model """

    def setUp(self):
        TvShow.objects.create(show_title='TestShow')

    def test_tvshow_exists(self):
        tvshow = TvShow.objects.get(show_title='TestShow')
        self.assertEqual(
            tvshow.get_show_info(), "TestShow")

"""
class TestUserTvShow(TestCase):

    def setUp(self):
        user = User.objects.create()
        TvShow.objects.create(show_title='TestShow')
"""