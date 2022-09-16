from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtPostsInfo, MgtUsersInfo
from django.conf import settings
import datetime
import json
import base64
import uuid
import traceback
from .libs import lib

# /Posts
class Posts(TemplateView):

    # 投稿一覧取得
    def get(self,request):
        try:
            if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                offset = int(request.GET.get('offset'))
                limit = offset + int(request.GET.get('limit'))
                posts = MgtPostsInfo.objects.all().order_by('created_at').reverse()[offset:limit]
            else:
                posts = MgtPostsInfo.objects.all().order_by('created_at').reverse()
            json_params = {}
            json_params['posts'] = []
            for post in posts:
                user = MgtUsersInfo.objects.get(user_id=post.user_id)
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
                        "prifliePicUrl": lib.create_url(user.profile_pic),
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
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # 新規投稿
    def post(self,request):
        try:
            data = json.loads(request.body)
            post_id = uuid.uuid4()

            # base64で送られてきたプロパティをデコードしてS3に格納
            if data['video'] is not None:
                with open('/mnt/goofys/videos/post{}.mp4'.format(post_id), 'wb') as f:
                    f.write(base64.b64decode(data['video']))
                video = 'videos/post/{}.mp4'.format(post_id)
            else:
                video = None
            if data['thumbnail'] is not None:
                with open('/mnt/goofys/pictures/thumbnail/{}.jpg'.format(post_id), 'wb') as f:
                    f.write(base64.b64decode(data['thumbnail']))
                thumbnail = 'pictures/thumbnail/{}.jpg'.format(post_id)
            else:
                thumbnail = None
            if data['sampleImage'] is not None:
                with open('/mnt/goofys/pictures/sample_image/{}.jpg'.format(post_id), 'wb') as f:
                    f.write(base64.b64decode(data['sampleImage']))
                sample_image = 'pictures/sample_image/{}.jpg'.format(post_id)
            else:
                sample_image = None
            
            dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
            post = MgtPostsInfo.objects.create(post_id=post_id, item_id=data['itemId'], item_name=data['itemName'], size_id=data['sizeId'], color_id=data['colorId'], category_id=data['categoryId'], description=data['description'], brand_id=data['brandId'], video=video, thumbnail=thumbnail, sample_image=sample_image, page_url=data['pageUrl'], user_id=data['userId'], created_at=dt_now, updated_at=dt_now)
            user = MgtUsersInfo.objects.get(user_id=data['userId'])
            json_params = {
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
                    "prifliePicUrl": lib.create_url(user.profile_pic),
                    "introduction": user.introduction,
                    "createdAt": str(user.created_at),
                    "updatedAt": str(user.updated_at)
                },
                "createdAt": str(post.created_at),
                "updatedAt": str(post.updated_at)
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

# /PostId
class PostId(TemplateView):

    # 投稿ID指定取得
    def get(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                post = MgtPostsInfo.objects.get(post_id=post_id)
                user = MgtUsersInfo.objects.get(user_id=post.user_id)
                json_params = {
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
                        "prifliePicUrl": lib.create_url(user.profile_pic),
                        "introduction": user.introduction,
                        "createdAt": str(user.created_at),
                        "updatedAt": str(user.updated_at)
                    },
                    "createdAt": str(post.created_at),
                    "updatedAt": str(post.updated_at)
                }
                status = 200
            else:
                json_params = {
                    "message": "post not exist",
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

    # 投稿削除
    def delete(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                post = MgtPostsInfo.objects.get(post_id=post_id)
                post.delete()
                status = 204
            else:
                json_params = {
                    "message": "post not exist"
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