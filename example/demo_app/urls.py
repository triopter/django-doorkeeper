from django.urls import path

from .views import HomeView, PublicView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("public/", PublicView.as_view(), name="public"),
]
