from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium import webdriver


class BasicTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.web_driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.web_driver.quit()

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")

    @tag("slow", "user")
    def test_login_able(self):
        self.web_driver.get(self.live_server_url)
        login_redirect = self.web_driver.find_element_by_css_selector(
            "#navbarNavDropdown > ul.nav.navbar-nav.navbar-right.myNavbarUl > li.navbar-register.login-li > a").get_attribute(
            "href")
        self.assertEqual(login_redirect, f"{self.live_server_url}/accounts/login/")


    @tag("slow", "user")
    def test_login(self):
        self.web_driver.get(f"{self.live_server_url}/accounts/login/")
        username_input = self.web_driver.find_element_by_css_selector("#id_login")
        password_input = self.web_driver.find_element_by_css_selector("#id_password")

        username_input.send_keys("testuser")
        password_input.send_keys("test12345")

        self.web_driver.find_element_by_css_selector("#login > div > form > div > div:nth-child(1) > button").click()
        self.assertEqual(self.web_driver.current_url, f"{self.live_server_url}/dashboards/homepage/")
        # try:
        #     x = WebDriverWait(self.web_driver, 10).until(expected_conditions.presence_of_all_elements_located(""))
        # except TimeoutException:
        #     assert ("Unable to load new page")
