from django.urls import path
from .views import Comments, CommentId

urlpatterns = [
    path('', Comments.as_view()),
    path('/<str:parameter>', CommentId.as_view()),
]