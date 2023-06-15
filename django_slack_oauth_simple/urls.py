from django.urls import path
from .views import OAuthView

urlpatterns = [
    path('login/', OAuthView.as_view(), name='slack_oauth'),
]
