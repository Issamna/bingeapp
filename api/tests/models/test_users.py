from django.test import TestCase
from bingeauth.models.user import User
from bingeauth.models.userprofile import UserProfile

class TestUserModels(TestCase):
    def setUp(self):
        self.email = "test@test.com"
        self.username = "test"
        self.password = "12345"
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_user_exists(self):
        self.assertTrue(User.objects.filter(email=self.email).exists(), True)

    def test_user_has_userprofile(self):
        self.assertTrue(self.user.userprofile.username, self.username)
