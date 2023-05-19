from django.urls import path
from .views import HomeView, ThanksView, ProjectsDetailView, LoginView, SignUpView, UserUpdateView, UserDeleteView, PasswordsChangeView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns= [
    path('', HomeView.as_view(), name='home'),
    path('thank_you/', ThanksView.as_view(), name='thanks'),
    path('projects_detail/', ProjectsDetailView.as_view(), name='projects_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('add/', SignUpView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', UserUpdateView.as_view(), name='edit_user'),
    path('delete/', UserDeleteView.as_view(), name='delete_user'),
    path('password/', PasswordsChangeView.as_view(), name='change_password'),

    path('password_reset/', PasswordResetView.as_view(
      template_name = 'password/password_reset.html'
    ), name='password_reset'),

    path('password_reset/done/', PasswordResetDoneView.as_view(
      template_name='password/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
      template_name='password/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', PasswordResetCompleteView.as_view(
      template_name='password/password_reset_complete.html'
    ), name='password_reset_complete'),
]
