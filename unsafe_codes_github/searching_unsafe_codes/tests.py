from django.test import TestCase
from .models import Settings, Unsafe_codes, Languages, Statuses, History
from users_and_permissions.models import AdvancedUser
from mixer.backend.django import mixer
from django.test import Client
from .templatetags import template_filters

# Create your tests here.
class SettingsTestCase(TestCase):

    def test_is_path_to_token(self):
        user = AdvancedUser.objects.create_user(username='test_user', email='test_email@email.com', password='123qwe123')
        setting = Settings.objects.create(author='test_author', phone=123123, email='test_email@email.com', create_user=user, path_to_token='qwe')
        self.assertTrue(setting.is_path_to_token())


class StatusTestCase(TestCase):

    def test_str(self):
        status = mixer.blend(Statuses, description='description')
        self.assertEqual(str(status), 'description')


class UnsafeCodesTestCase(TestCase):

    def setUp(self):
        #user = AdvancedUser.objects.create_user(username='test_user', email='test_email@email.com', password='123qwe123')
        self.unsafe_code = mixer.blend(Unsafe_codes,
                                       language = mixer.blend(Languages),
                                       string_code = 'string_code',
                                       description = 'description',
                                       add_description = 'add_description',
                                       status = mixer.blend(Statuses))

    def test_is_language(self):
        self.assertTrue(self.unsafe_code.is_language())

    def test_is_string_code(self):
        self.assertTrue(self.unsafe_code.is_string_code())

    def test_is_description(self):
        self.assertTrue(self.unsafe_code.is_description())

    def test_is_status(self):
        self.assertTrue(self.unsafe_code.is_status())


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = AdvancedUser.objects.create_user(username='test_user', email='test_email@email.com', password='123qwe123')

    def test_main(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contacts(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_create_contact(self):
        response = self.client.post('/contacts_create/',
                                    author='test_author',
                                    phone=123123,
                                    email='test_email@email.com',
                                    create_user=self.user,
                                    path_to_token='qwe')
        self.assertEqual(response.status_code, 302)

    def test_unlogin_user(self):
        response = self.client.get('/contacts_create/')
        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get('/contacts_create/')
        self.assertEqual(response.status_code, 302)

    def test_login_superuser(self):
        AdvancedUser.objects.create_superuser(username='test_superuser', email='test_superemail@email.com', password='123qwe123')
        self.client.login(username='test_superuser', password='123qwe123')
        response = self.client.get('/contacts_create/')
        self.assertEqual(response.status_code, 200)


class HistoryTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = AdvancedUser.objects.create_user(username='test_user', email='test_email@email.com', password='123qwe123')

    def test_create_history(self):
        History(params='settings', user=self.user).save()
        result = History.objects.all()
        self.assertGreater(result.count(), 0)


class TemplateFiltersTest(TestCase):

    def setUp(self) -> None:
        self.user_settings = 'eval;sqlite3;pickle;EMAIL_HOST_USER;EMAIL_HOST_PASSWORD;'
        self.unsafe_code = mixer.blend(Unsafe_codes,
                                       language = mixer.blend(Languages),
                                       string_code = 'sqlite3',
                                       description = 'description',
                                       add_description = 'add_description',
                                       status = mixer.blend(Statuses))

    def test_get_user_settings(self):
        user_settings_list = template_filters.get_user_settings(self.user_settings)
        self.assertGreater(len(user_settings_list), 0)