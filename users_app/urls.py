from django.urls import path
from .views import Users, UserId, UserIdPosts

urlpatterns = [
    path('', Users.as_view()),
    path('<str:parameter>', UserId.as_view()),
    path('<str:parameter>/posts', UserIdPosts.as_view()),
]