from django.urls import path
from .views import Users, UserId

urlpatterns = [
    path('', Users.as_view()),
    path('<str:parameter>', UserId.as_view()),
]