from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtUsersInfo, MgtPostsInfo
from django.conf import settings
from django.db.models import Q
import os
import datetime
import json
import traceback
from .libs import lib

# /users
class Users(TemplateView):
    # ユーザ一覧取得（作成中）
    def get(self,request):
        # hoge = MgtUsersInfo.objects.get(user_id='test2')
        # json_params = {
        #     'message': hoge.gender.gender_id
        # }
        # # status = 200
        # # hoge = settings.PITTA_ENV
        # json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
        # return HttpResponse(str(vars(hoge.gender)), status=200) 
        tmp = "boneTypeId"
        json_str = lib.conversion_from_camel_to_snake(tmp)
        return HttpResponse(json_str, status=200) 

    # ユーザ新規登録
    def post(self,request):
        try:
            data = json.loads(request.body)
            dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
            user = MgtUsersInfo.objects.create(user_id=data['userId'], email=data['email'], created_at=dt_now, updated_at=dt_now)
            json_params = {
                "userId": user.user_id,
                "email": user.email
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

# /users/<userId>
class UserId(TemplateView):

    # ユーザ情報取得
    def get(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                json_params = {
                    "userId": user.user_id,
                    "email": user.email,
                    "name": user.name,
                    "genderId": user.gender_id,
                    "age": user.age,
                    "height": user.height,
                    "weight": user.weight,
                    "boneTypeId": user.bone_type_id,
                    "profliePicUrl": lib.create_url(user.profile_pic),
                    "introduction": user.introduction,
                    "createdAt": str(user.created_at),
                    "updatedAt": str(user.updated_at)
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

    # ユーザ情報更新
    def put(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                data = json.loads(request.body)

                # リクエスト内容を元にユーザ情報を更新する
                for key, value in data.items():
                    if key == "email" and value is not None:
                        user.email = value if len(str(value)) != 0 else None
                    elif key == "name" and value is not None:
                        user.name = value if len(str(value)) != 0 else None
                    elif key == "genderId" and value is not None:
                        user.gender_id = value if len(str(value)) != 0 else None
                    elif key == "age" and value is not None:
                        user.age = value if len(str(value)) != 0 else None
                    elif key == "height" and value is not None:
                        user.height = value if len(str(value)) != 0 else None
                    elif key == "weight" and value is not None:
                        user.weight = value if len(str(value)) != 0 else None
                    elif key == "boneTypeId" and value is not None:
                        user.bone_type_id = value if len(str(value)) != 0 else None
                    elif key == "profilePic" and value is not None:
                        if len(str(value)) != 0:
                            user.profile_pic = lib.decode_and_storage(value, 'pictures/profile_pics', user.user_id)
                        else:
                            user.profile_pic = None
                    elif key == "introduction" and value is not None:
                        user.introduction = value if len(str(value)) != 0 else None
                
                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                user.updated_at = dt_now
                user.save()
                json_params = {
                    "userId": user.user_id,
                    "email": user.email,
                    "name": user.name,
                    "genderId": user.gender_id,
                    "age": user.age,
                    "height": user.height,
                    "weight": user.weight,
                    "boneTypeId": user.bone_type_id,
                    "profliePicUrl": lib.create_url(user.profile_pic),
                    "introduction": user.introduction,
                    "createdAt": str(user.created_at),
                    "updatedAt": str(user.updated_at)
                }
                status = 200
            else:
                json_params = {
                    "message": "user not exist"
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

    # ユーザ削除
    def delete(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                user.delete()
                status = 204
            else:
                json_params = {
                    "message": "user not exist"
                }
                status = 404
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

# /users/<userId>/posts
class UserIdPosts(TemplateView):

    # ユーザ投稿動画取得
    def get(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                    offset = int(request.GET.get('offset'))
                    limit = offset + int(request.GET.get('limit'))
                    posts = MgtPostsInfo.objects.filter(user_id=user_id).order_by('created_at').reverse()[offset:limit]
                else:
                    posts = MgtPostsInfo.objects.filter(user_id=user_id).order_by('created_at').reverse()
                json_params = {}
                json_params['posts'] = []
                for post in posts:
                    json_param = {
                        "postId": str(post.post_id),
                        "itemId": post.item_id,
                        "itemName": post.item_name,
                        "sizeId": post.size_id,
                        "colorId": post.color_id,
                        "categoryId": post.category_id,
                        "description": post.description,
                        "brandId": post.brand_id,
                        "videoUrl": lib.create_url(post.video),
                        "thumbnailUrl": lib.create_url(post.thumbnail),
                        "sampleImageUrl": lib.create_url(post.sample_image),
                        "pageUrl": post.page_url,
                        "user": {
                            "userId": user.user_id,
                            "email": user.email,
                            "name": user.name,
                            "genderId": user.gender_id,
                            "age": user.age,
                            "height": user.height,
                            "weight": user.weight,
                            "boneTypeId": user.bone_type_id,
                            "profliePicUrl": lib.create_url(user.profile_pic),
                            "introduction": user.introduction,
                            "createdAt": str(user.created_at),
                            "updatedAt": str(user.updated_at)
                        },
                        "createdAt": str(post.created_at),
                        "updatedAt": str(post.updated_at)
                    }
                    json_params['posts'].append(json_param)
                json_params['total'] = len(json_params['posts'])
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
