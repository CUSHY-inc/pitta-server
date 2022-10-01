from django.urls import path
from .views import Templates, TemplateId

urlpatterns = [
    path('', Templates.as_view()),
    path('/<str:parameter>', TemplateId.as_view()),
]