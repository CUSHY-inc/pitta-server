from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtUsersInfo, MgtPostsInfo, MgtTemplatesInfo, MgtLikesInfo, MgtCommentsInfo
from django.conf import settings
from django.db.models import Q
import os
import datetime
import json
import traceback
from .libs import lib

# /users
class Users(TemplateView):
    # ユーザ一覧取得
    def get(self,request):
        try:
            if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                offset = int(request.GET.get('offset'))
                limit = offset + int(request.GET.get('limit'))
            else:
                offset = lib.offset
                limit = lib.limit
            users = MgtUsersInfo.objects.all().order_by('created_at').reverse()[offset:limit]
            json_params = []
            for user in users:
                json_param = {
                    "userId": user.user_id,
                    "email": user.email,
                    "name": user.name,
                    "genderId": user.gender_id,
                    "age": user.age,
                    "height": user.height,
                    "weight": user.weight,
                    "boneTypeId": user.bone_type_id,
                    "profilePicUrl": lib.create_url(user.profile_pic),
                    "profilePic": None,
                    "introduction": user.introduction,
                    "createdAt": str(user.created_at),
                    "updatedAt": str(user.updated_at)
                }
                json_params.append(json_param)
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

    # ユーザ新規登録
    def post(self,request):
        try:
            data = json.loads(request.body)
            # ユーザ作成
            dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
            user = MgtUsersInfo.objects.create(user_id=data['userId'], email=data['email'], created_at=dt_now, updated_at=dt_now)
            # user_id/email以外の情報もあれば更新する
            for key, value in data.items():
                if key == "name" and value is not None:
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
                "profilePicUrl": lib.create_url(user.profile_pic),
                "profilePic": None,
                "introduction": user.introduction,
                "createdAt": str(user.created_at),
                "updatedAt": str(user.updated_at)
            }
            status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

    # ユーザ情報更新
    def put(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data['userId']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)

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
                    "profilePicUrl": lib.create_url(user.profile_pic),
                    "profilePic": None,
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
            return HttpResponse(json_str, status=status, content_type="application/json")

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
                    "profilePicUrl": lib.create_url(user.profile_pic),
                    "profilePic": None,
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
            return HttpResponse(json_str, status=status, content_type="application/json")

    # ユーザ削除
    def delete(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                user.delete()
                lib.delete_file('pictures/profile_pics', user_id)
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
                return HttpResponse(status=status, content_type="application/json")
            else:
                json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
                return HttpResponse(json_str, status=status, content_type="application/json")

# /users/<userId>/posts
class Posts(TemplateView):

    # ユーザ投稿動画取得
    def get(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                    offset = int(request.GET.get('offset'))
                    limit = offset + int(request.GET.get('limit'))
                else:
                    offset = lib.offset
                    limit = lib.limit
                posts = MgtPostsInfo.objects.filter(user_id=user_id).order_by('created_at').reverse()[offset:limit]
                json_params = []
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
                        "video": None,
                        "thumbnailUrl": lib.create_url(post.thumbnail),
                        "thumbnail": None,
                        "sampleImageUrl": post.sample_image_url,
                        "pageUrl": post.page_url,
                        "totalLikes": MgtLikesInfo.objects.filter(post_id=post.post_id).count(),
                        "totalComments": MgtCommentsInfo.objects.filter(post_id=post.post_id).count(),
                        "user": {
                            "userId": user.user_id,
                            "email": user.email,
                            "name": user.name,
                            "genderId": user.gender_id,
                            "age": user.age,
                            "height": user.height,
                            "weight": user.weight,
                            "boneTypeId": user.bone_type_id,
                            "profilePicUrl": lib.create_url(user.profile_pic),
                            "profilePic": None,
                            "introduction": user.introduction,
                            "createdAt": str(user.created_at),
                            "updatedAt": str(user.updated_at)
                        },
                        "createdAt": str(post.created_at),
                        "updatedAt": str(post.updated_at)
                    }
                    json_params.append(json_param)
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
            return HttpResponse(json_str, status=status, content_type="application/json")

# /users/<userId>/templates
class Templates(TemplateView):

    # ユーザテンプレート取得
    def get(self, request, **kwargs):
        try:
            user_id = kwargs['parameter']
            if MgtUsersInfo.objects.filter(user_id=user_id).exists():
                user = MgtUsersInfo.objects.get(user_id=user_id)
                if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                    offset = int(request.GET.get('offset'))
                    limit = offset + int(request.GET.get('limit'))
                else:
                    offset = lib.offset
                    limit = lib.limit  
                templates = MgtTemplatesInfo.objects.filter(user_id=user_id).order_by('created_at').reverse()[offset:limit]
                json_params = []
                for template in templates:
                    json_param = {
                        "templateId": template.template_id,
                        "userId": template.user_id,
                        "text": template.text,
                        "createdAt": str(template.created_at),
                        "updatedAt": str(template.updated_at)
                    }
                    json_params.append(json_param)
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
            return HttpResponse(json_str, status=status, content_type="application/json")
