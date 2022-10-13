from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtGenderList, MgtBoneTypeList, MgtSizeList, MgtColorList, MgtCategoryList, MgtBrandList
import json
import traceback

# /masters/genderList
class GenderList(TemplateView):
    def get(self,request):
        try:
            gender_list = MgtGenderList.objects.all().order_by('gender_id')
            json_params = {}
            json_params['list'] = []
            for item in gender_list:
                json_param = {
                    "genderId": item.gender_id,
                    "gender": item.gender
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

# /masters/boneTypeList
class BoneTypeList(TemplateView):
    def get(self,request):
        try:
            bone_type_list = MgtBoneTypeList.objects.all().order_by('bone_type_id')
            json_params = {}
            json_params['list'] = []
            for item in bone_type_list:
                json_param = {
                    "boneTypeId": item.bone_type_id,
                    "boneType": item.bone_type
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

# /masters/sizeList
class SizeList(TemplateView):
    def get(self,request):
        try:
            size_list = MgtSizeList.objects.all().order_by('size_id')
            json_params = {}
            json_params['list'] = []
            for item in size_list:
                json_param = {
                    "sizeId": item.size_id,
                    "size": item.size
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

# /masters/colorList
class ColorList(TemplateView):
    def get(self,request):
        try:
            color_list = MgtColorList.objects.all().order_by('color_id')
            json_params = {}
            json_params['list'] = []
            for item in color_list:
                json_param = {
                    "colorId": item.color_id,
                    "color": item.color
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

# /masters/categoryList
class CategoryList(TemplateView):
    def get(self,request):
        try:
            category_list = MgtCategoryList.objects.all().order_by('category_id')
            json_params = {}
            json_params['list'] = []
            for item in category_list:
                json_param = {
                    "categoryId": item.category_id,
                    "category": item.category
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

# /masters/brandList
class BrandList(TemplateView):
    def get(self,request):
        try:
            brand_list = MgtBrandList.objects.all().order_by('brand_id')
            json_params = {}
            json_params['list'] = []
            for item in brand_list:
                json_param = {
                    "brandId": item.brand_id,
                    "brand": item.brand
                }
                json_params['list'].append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")