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
            i = 0
            for item in gender_list:
                json_params[i] = {}
                json_params[i]['gender_id'] = item.gender_id
                json_params[i]['gender'] = item.gender
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/boneTypeList
class BoneTypeList(TemplateView):
    def get(self,request):
        try:
            bone_type_list = MgtBoneTypeList.objects.all().order_by('bone_type_id')
            json_params = {}
            i = 0
            for item in bone_type_list:
                json_params[i] = {}
                json_params[i]['bone_type_id'] = item.bone_type_id
                json_params[i]['bone_type'] = item.bone_type
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/sizeList
class SizeList(TemplateView):
    def get(self,request):
        try:
            size_list = MgtSizeList.objects.all().order_by('size_id')
            json_params = {}
            i = 0
            for item in size_list:
                json_params[i] = {}
                json_params[i]['size_id'] = item.size_id
                json_params[i]['size'] = item.size
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/colorList
class ColorList(TemplateView):
    def get(self,request):
        try:
            color_list = MgtColorList.objects.all().order_by('color_id')
            json_params = {}
            i = 0
            for item in color_list:
                json_params[i] = {}
                json_params[i]['color_id'] = item.color_id
                json_params[i]['color'] = item.color
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/categoryList
class CategoryList(TemplateView):
    def get(self,request):
        try:
            category_list = MgtCategoryList.objects.all().order_by('category_id')
            json_params = {}
            i = 0
            for item in category_list:
                json_params[i] = {}
                json_params[i]['category_id'] = item.category_id
                json_params[i]['category'] = item.category
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/brandList
class BrandList(TemplateView):
    def get(self,request):
        try:
            brand_list = MgtBrandList.objects.all().order_by('brand_id')
            json_params = {}
            i = 0
            for item in brand_list:
                json_params[i] = {}
                json_params[i]['brand_id'] = item.brand_id
                json_params[i]['brand'] = item.brand
                i += 1
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)