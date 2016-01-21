from allauth.account.adapter import DefaultAccountAdapter
from telentapp.models import Settings

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        allow_signup = Settings.objects.get_or_create()[0].allow_signup
        return allow_signup