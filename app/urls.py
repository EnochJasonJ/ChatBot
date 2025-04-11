from django.urls import path
from .views import AskAI , register,Login
urlpatterns = [
    path('chat/',AskAI.as_view(),name="chat"),
    path('register/',register.as_view(),name="register"),
    path("login/",Login.as_view(),name="login")
]

