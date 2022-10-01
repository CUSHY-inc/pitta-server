from django.urls import path
from .views import Likes, LikeId

urlpatterns = [
    path('', Likes.as_view()),
    path('/<str:parameter>', LikeId.as_view()),
]