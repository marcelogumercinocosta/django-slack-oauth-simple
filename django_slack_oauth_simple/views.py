import uuid
import requests
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic.base import RedirectView
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import  login

def gather_slack_info(user_object):
    slack_user = user_object["user"]
    slack_team = user_object["team"]
    print(user_object)
    context = {
        "slack_id": slack_user["id"],
        "name": slack_user["name"],
        "email": slack_user["email"],
        "team_id": slack_team["id"],
        "team_name": slack_team["name"],
        "domain": slack_team["domain"],
        "avatar": slack_user["image_24"]
    }
    return context


class OAuthView(RedirectView):
    permanent = True
    text_error = 'Something went wrong with updating your authorization.'

    def dispatch(self, request, *args, **kwargs):
        return super(OAuthView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        code = request.GET.get('code')
        if not code:
            return self.auth_request()
        self.validate_state(request.GET.get('state'))
        access_content = self.oauth_access(code)
        if not access_content.status_code == 200:
            return self.error_message()
        api_data = access_content.json()
        if not api_data['ok']:
            return self.error_message(api_data['error'])
        user_obj = gather_slack_info(api_data)
        profile = self.verify(user_obj)
        login(request, profile)
        messages.add_message(self.request, messages.SUCCESS, 'Your account has been successfully updated.')                                        
        return HttpResponseRedirect(reverse("home"))

    def auth_request(self):
        state = self.store_state()
        params = urlencode({
            'client_id': settings.SLACK_CLIENT_ID,
            'redirect_uri': self.request.build_absolute_uri(reverse('slack_oauth')),
            'scope': 'identity.basic identity.email identity.team identity.avatar',
            'state': state
        })
        return self.response(settings.SLACK_AUTHORIZATION_URL + '?' + params)

    def oauth_access(self, code):
        params = {
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': self.request.build_absolute_uri(reverse('slack_oauth'))
        }
        return requests.get(settings.SLACK_OAUTH_ACCESS_URL, params=params)

    def validate_state(self, state):
        state_before = self.request.session.pop('state')
        if state_before != state:
            raise ValidationError('State mismatch upon authorization completion. Try new request.')
        return True

    def store_state(self):
        state = str(uuid.uuid4())[:6]
        self.request.session["state"] = state
        return state

    def response(self, redirect='/'):
        return HttpResponseRedirect(redirect)


    def verify(self,user_obj):
        profile = get_user_model().objects.filter(username=user_obj["name"]).first()
        if profile is None:
            profile = get_user_model().objects.create(username=user_obj["name"], email=user_obj["email"])
            if not hasattr(profile, 'slack_id'):
                raise ValidationError('The User Model does not have the attribute slack_id.')
            profile.slack_id=user_obj["slack_id"]
            profile.save()
        if hasattr(profile, 'team_name') and profile.team_name != user_obj["team_name"]:
            profile.team_name = user_obj["team_name"]
            profile.save()
        if hasattr(profile, 'avatar') and profile.team_name != user_obj["avatar"]:
            profile.team_name = user_obj["avatar"]
            profile.save()
        return profile
                