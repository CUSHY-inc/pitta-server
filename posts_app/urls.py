from django.urls import path
from .views import Posts, PostId

urlpatterns = [
        path('', Posts.as_view()),
        path('<str:parameter>', PostId.as_view()),
]