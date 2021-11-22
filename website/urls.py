from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('requests', views.requests, name="requests"),
    path('rejrequest', views.reject, name="rejrequest"),
    path('accrequest', views.accept, name="accrequest"),
    path('login', views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
]