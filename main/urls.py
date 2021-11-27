from django.urls import path

from main import views

urlpatterns = [
    path('GetMovie/<str:username>', views.UserPrediction.as_view()),
]
