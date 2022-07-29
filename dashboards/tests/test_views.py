from django.contrib.auth.models import User
from django.test import TransactionTestCase, Client


class LoginTestCase(TransactionTestCase):
    client = Client()

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword1234")

    def tearDown(self):
        self.user.delete()

    def test_root(self):
        response = self.client.get("/")  # get the homepage
        self.assertEqual(response.status_code, 200)

    def test_login_root(self):
        self.client.login(username="testuser", password="testpassword1234")
        response = self.client.get("/")  # get the homepage
        self.assertRedirects(response, "/dashboards/integrations", status_code=302, target_status_code=301)


