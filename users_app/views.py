from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtUsersInfo
from django.conf import settings
from django.db.models import Q
import os
import datetime
import json
import boto3
import base64
import uuid
import re
import zipfile

# /Users
class Users(TemplateView):
    # ユーザ一覧取得（作成中）
    def get(self,request):
        hoge = MgtUsersInfo.objects.get(user_id='test1')
        json_params = {
            'users': [
                {
                    'hoge1': 'hoge1',
                    'hoge2': 'hoge2',
                }
            ],
            'result':0x0000,
            'message':"test",
        }
        status = 200
        hoge = settings.PITTA_ENV
        json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
        return HttpResponse(hoge, status=200) 

    # ユーザ新規登録
    def post(self,request):
        try:
            user_id = request.POST.get('userId')
            email = request.POST.get('email')
            dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
            MgtUsersInfo.objects.create(user_id=user_id, email=email, created_at=dt_now, updated_at=dt_now)
            json_params = {
                'code':0x0000,
                'message':"success",
            }
            status = 200
        except Exception as e:
            json_params = {
                'code':0x0001,
                'message':str(e),
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

# /Users/<UserId>
class UserId(TemplateView):

    # ユーザ情報取得(user_id or email)
    def get(self, request, **kwargs):
        try:
            user_identilier = kwargs['parameter']
            if MgtUsersInfo.objects.filter(Q(user_id=user_identilier) | Q(email=user_identilier)).exists():
                user = MgtUsersInfo.objects.get(Q(user_id=user_identilier) | Q(email=user_identilier))
                pic_url = ''
                if user.profile_pic is not None:
                    if len(user.profile_pic) != 0:
                        s3_client = boto3.client('s3')
                        BUCKET = settings.PITTA_ENV
                        OBJECT = user.profile_pic
                        pic_url = s3_client.generate_presigned_url(
                            'get_object',
                            Params={'Bucket': BUCKET, 'Key': OBJECT},
                            ExpiresIn=300)
                json_params = {
                    'user': [
                        {
                            'userId': user.user_id,
                            'email': user.email,
                            'userName': user.user_name,
                            'gender': user.gender,
                            'age': user.age,
                            'height': user.height,
                            'weight': user.weight,
                            'boneType': user.bone_type,
                            'prifliePic': pic_url,
                            'introduction': user.introduction,
                            'createdAt': str(user.created_at),
                            'updatedAt': str(user.updated_at)
                        }
                    ],
                    'total': 12,
                    'code':0x0000,
                    'message':'success',
                }
                status = 200
            else:
                json_params = {
                    'code':0x0001,
                    'message':'user not exist',
                }
                status = 404
        except Exception as e:
            json_params = {
                'code':0x0001,
                'message':str(e),
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # ユーザ情報更新
    def post(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                for key, value in request.POST.items():
                    if key == "email":
                        user.email = value
                    elif key == "userName":
                        user.user_name = value
                    elif key == "gender":
                        user.gender = value
                    elif key == "age":
                        user.age = value
                    elif key == "height":
                        user.height = value
                    elif key == "weight":
                        user.weight = value
                    elif key == "boneType":
                        user.bone_type = value
                    elif key == "profilePic":
                        pre_pic = user.profile_pic
                        if len(value) != 0:
                            s = value
                            id = uuid.uuid4()
                            with open('/mnt/goofys/pictures/{}.jpg'.format(id), 'wb') as f:
                                f.write(base64.b64decode(s))
                            user.profile_pic = 'pictures/{}.jpg'.format(id)
                        else:
                            user.profile_pic = ''
                    elif key == "introduction":
                        user.introduction = value
                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                user.updated_at = dt_now
                user.save()
                if pre_pic is not None:
                    if len(pre_pic) != 0:
                        if(os.path.isfile('/mnt/goofys/{}'.format(pre_pic))):
                            os.remove('/mnt/goofys/{}'.format(pre_pic))
                json_params = {
                    'code':0x0000,
                    'message':'success',
                }
                status = 200
            else:
                json_params = {
                    'code':0x0001,
                    'message':'user not exist',
                }
                status = 404
        except Exception as e:
            json_params = {
                'code':0x0001,
                'message':str(e),
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # ユーザ削除
    def delete(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                user.delete()
                json_params = {
                    'code':0x0000,
                    'message':'success',
                }
                status = 200
            else:
                json_params = {
                    'code':0x0001,
                    'message':'user not exist',
                }
                status = 404
        except Exception as e:
            json_params = {
                'code':0x0001,
                'message':str(e),
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)
