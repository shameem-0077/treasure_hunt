from django.urls import path
from hunts import views


app_name = "api_v1_hunts"
urlpatterns = [
    path('user-question/', views.get_user_question),
    path('validate-user-question/', views.validate_user_question),
    path('list-solved-question-answers/', views.validate_user_question),
]