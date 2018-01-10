from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class TestBackend(object):
    """
    定义自己的认证方式
    但是还是要从User中初始化用户
    """

    def authenticate(self, request, username=None, password=None):
        # todo 此处应可以改成 cas

        if password == 'dapianzi':
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password is always 'dapianzi'.
                user = User(username=username)
                user.is_staff = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None