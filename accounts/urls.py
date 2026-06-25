from django.urls import path
from . views import (
    RegisterView,
    verify_email_view,
    LoginView,
    RefreshTokenView
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path(
        "verify/<str:token>/", verify_email_view, name="verify-email",
    ),
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshTokenView.as_view())
]
