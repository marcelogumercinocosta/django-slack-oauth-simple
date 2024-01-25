## Instructions

1. Install using pip:

    ```
    $ pip install git+https://github.com/marcelogumercinocosta/django-slack-oauth-simple.git

2. Add `django_slack_oauth` to `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = (
        ...
        'django_slack_oauth_simple',
    )

3. Add Slack OAuth base url to your project's `urls.py`:

    ```python
    urlpatterns = [
        ...
        path("slack/", include("django_slack_oauth_simple.urls")),
        ...
    ]
    ```

4. Specify your Slack credentials and OAuth Scope in `settings.py`:

    ```python
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
    SLACK_SCOPE = 'admin,bot'
    ```
    If you aren't sure what your scope should be, read more about [Slack OAuth Scopes](https://api.slack.com/docs/oauth-scopes).


## Example

Add a link to Slack OAuth in one of your templates:

```
<a href='{% url 'slack_oauth' %}'>Get slacked</a>
