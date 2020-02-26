from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    path("createuser", views.createUser),
    path("mainpage", views.mainpage),
    path("login", views.login),
    path("logout", views.logout),
    path("travels/add", views.travelCreate),
    path("taveladd", views.travelAdd),
    path("jointrip/<int:travelid>", views.joinTrip),
    path("travel/destination<int:travelid>", views.tripDetail)
]