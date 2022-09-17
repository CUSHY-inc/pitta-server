from django.urls import path
from .views import GenderList, BoneTypeList, SizeList, ColorList, CategoryList, BrandList

urlpatterns = [
    path('genderList/', GenderList.as_view()),
    path('boneTypeList/', BoneTypeList.as_view()),
    path('sizeList/', SizeList.as_view()),
    path('colorList/', ColorList.as_view()),
    path('categoryList/', CategoryList.as_view()),
    path('brandList/', BrandList.as_view()),
]