from django.urls import path
from users import views

app_name = "api_v1_users"
urlpatterns = [
    path('signup/', views.create_account),
    path('login/', views.login_account),
]