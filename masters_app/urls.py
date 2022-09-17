from django.urls import path
from .views import genderList, boneTypeList, sizeList, colorList, categoryList, brandList

urlpatterns = [
    path('genderList/', genderList.as_view()),
    path('boneTypeList/', boneTypeList.as_view()),
    path('sizeList/', sizeList.as_view()),
    path('colorList/', colorList.as_view()),
    path('categoryList/', categoryList.as_view()),
    path('brandList/', brandList.as_view()),
]