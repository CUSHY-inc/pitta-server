from django.urls import path
from .views import Posts, PostId, Likes, Comments

urlpatterns = [
        path('', Posts.as_view()),
        path('<str:parameter>', PostId.as_view()),
        path('<str:parameter>/likes', Likes.as_view()),
        path('<str:parameter>/comments', Comments.as_view()),
]