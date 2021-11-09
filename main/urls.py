from django.urls import path

from main import views

urlpatterns = [
    path('GetMovie/<str:user_id>', views.UserPrediction.as_view()),
]
