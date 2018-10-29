from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('signup/', views.signup_view, name='signup-view'),
    path('profile/', views.profile, name='profile'),
    path('facebook-login/', views.facebook_login, name='facebook-login')
]