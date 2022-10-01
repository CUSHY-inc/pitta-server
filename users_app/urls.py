from django.urls import path
from .views import Users, UserId, UserIdPosts, UserIdTemplates

urlpatterns = [
    path('', Users.as_view()),
    path('/<str:parameter>', UserId.as_view()),
    path('/<str:parameter>/posts', UserIdPosts.as_view()),
    path('/<str:parameter>/templates', UserIdTemplates.as_view()),
]