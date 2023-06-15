from django.conf import settings

default_settings = {
    'SLACK_CLIENT_ID': None,
    'SLACK_CLIENT_SECRET': None,
    'AUTH_USER_MODEL': None,
    'SLACK_AUTHORIZATION_URL': 'https://slack.com/oauth/authorize',
    'SLACK_OAUTH_ACCESS_URL': 'https://slack.com/api/oauth.access',
    'SLACK_SUCCESS_REDIRECT_URL': '/',
    'SLACK_ERROR_REDIRECT_URL': '/',

    'SLACK_SCOPE': 'identify,read,post',
}

class Settings(object):
    def __init__(self, defaults):
        for k, v in defaults.items():
            if hasattr(settings, k):
                if getattr(settings, k) == None:
                    raise SyntaxError("Mensagem de erro personalizada")
            else:
                setattr(settings, k, v )

settings_obj = Settings(default_settings)
