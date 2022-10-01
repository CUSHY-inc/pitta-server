from django.urls import path
from .views import Users, UserId, Posts, Templates

urlpatterns = [
    path('', Users.as_view()),
    path('/<str:parameter>', UserId.as_view()),
    path('/<str:parameter>/posts', Posts.as_view()),
    path('/<str:parameter>/templates', Templates.as_view()),
]