from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtUsersInfo, MgtTemplatesInfo
from django.conf import settings
from django.db.models import Q
import os
import datetime
import json
import traceback

# /templates
class Templates(TemplateView):

    # ユーザテンプレート登録
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data['userId']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                data = json.loads(request.body)
                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                template = MgtTemplatesInfo.objects.create(user_id=user_id, text=data['text'], created_at=dt_now, updated_at=dt_now)
                json_params = {
                    "templateId": str(template.template_id),
                    "userId": template.user_id,
                    "text": template.text,
                    "createdAt": str(template.created_at),
                    "updatedAt": str(template.updated_at)
                }
                status = 200
            else:
                json_params = {
                    "message": "user not exist",
                }
                status = 404
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /templates/templateId
class TemplateId(TemplateView):

    # ユーザテンプレート更新
    def put(self, request, **kwargs):
        try:
            template_id = kwargs['parameter']
            data = json.loads(request.body)
            user_id = data['userId']
            if not MgtUsersInfo.objects.filter(user_id=user_id).exists():
                json_params = {
                    "message": "user not exist",
                }
                status = 404
            elif not MgtTemplatesInfo.objects.filter(template_id=template_id).exists():
                json_params = {
                    "message": "template not exist",
                }
                status = 404
            else:
                data = json.loads(request.body)
                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                template = MgtTemplatesInfo.objects.get(template_id=template_id)
                template.user_id = user_id
                template.text = data['text']
                template.updated_at = dt_now
                template.save()
                json_params = {
                    "templateId": str(template.template_id),
                    "userId": str(template.user_id),
                    "text": template.text,
                    "createdAt": str(template.created_at),
                    "updatedAt": str(template.updated_at)
                }
                status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # ユーザテンプレート削除
    def delete(self, request, **kwargs):
        try:
            template_id = kwargs['parameter']
            if not MgtTemplatesInfo.objects.filter(template_id=template_id).exists():
                json_params = {
                    "message": "template not exist",
                }
                status = 404
            else:
                template = MgtTemplatesInfo.objects.get(template_id=template_id)
                template.delete()                
                status = 204
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            if status == 204:
                return HttpResponse(status=status)
            else:
                json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
                return HttpResponse(json_str, status=status)


