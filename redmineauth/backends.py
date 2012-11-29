import re
import requests

from django.conf import settings

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()



class Redmine(object):
    """ Logs into a given Redmine site and creates
    a new user based on a successful login there """

    supports_object_permissions = False
    supports_inactive_user = False
    supports_anonymous_user = False

    def __init__(self):
        self.login_url = settings.REDMINE_URL + '/login'

    def extract_account_field(self, page, input_name):
        regex = '<input[^>]*? name="%s"[^>]*? value="([^"]*)" />' % re.escape(input_name)
        res = re.findall(regex, page)
        print input_name, res
        if res:
            return res[0]
        return ''

    def extract_account_info(self, page):
        """
        Parse user info from the account page
        """
        field_map = {
            'email': 'user[mail]',
            'first_name': 'user[firstname]',
            'last_name': 'user[lastname]',
        }
        return dict((dj, self.extract_account_field(page, rm)) for dj, rm in field_map.items())

    def authenticate(self, username=None, password=None):
        # Pass in the form data to our Redmine url
        account_url = settings.REDMINE_URL + '/my/account'
        data = {
            'username': username,
            'password': password,
            'back_url': account_url,
        }
        session = requests.session()
        response = session.post(self.login_url, data)

        # see if we're forwarded to the account page
        if response.history and \
            response.history[0].status_code==302 and \
            response.history[0].headers['location']==account_url:

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user_info = self.extract_account_info(response.text)
                user = User(username=username, **user_info)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            else:
                if not user.has_usable_password():
                    user.set_password(password)
                    user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None