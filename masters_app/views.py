from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtGenderList, MgtBoneTypeList
import json

# /masters/genderList
class genderList(TemplateView):
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
        except Exception as e:
            json_params = {
                "message": str(e)
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /masters/boneTypeList
class boneTypeList(TemplateView):
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
        except Exception as e:
            json_params = {
                "message": str(e)
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)