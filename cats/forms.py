from django.forms import Form

class SigninForm(Form):

    def is_valid(self):
        return True

    def is_multipart(self):
        return False
