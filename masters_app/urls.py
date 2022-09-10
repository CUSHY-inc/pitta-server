from django.urls import path
from .views import genderList, boneTypeList

urlpatterns = [
    path('genderList/', genderList.as_view()),
    path('boneTypeList/', boneTypeList.as_view()),
]