from django.contrib.auth import views
from django.urls import path

from .views import CustomLoginView, ProfileView, UserUpdate

app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/update/', UserUpdate.as_view(), name='update'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
