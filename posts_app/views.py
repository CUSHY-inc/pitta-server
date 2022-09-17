from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtPostsInfo, MgtUsersInfo, MgtLikesInfo, MgtCommentsInfo
from django.db.models import Q
import datetime
import json
import uuid
import traceback
from .libs import lib

# /posts
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

            # base64で送られてきたデータをデコードしてS3に格納
            if data['video'] is not None:
                video = lib.decode_and_storage(data['video'], 'videos/posts', post_id)
            else:
                video = None
            if data['thumbnail'] is not None:
                thumbnail = lib.decode_and_storage(data['thumbnail'], 'pictures/thumbnails', post_id)
            else:
                thumbnail = None
            if data['sampleImage'] is not None:
                sample_image = lib.decode_and_storage(data['sampleImage'], 'pictures/sample_images', post_id)
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
                    "profliePicUrl": lib.create_url(user.profile_pic),
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

# /posts/postId
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
                        "profliePicUrl": lib.create_url(user.profile_pic),
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

# /posts/postId/likes
class Likes(TemplateView):

    # いいね一覧取得
    def get(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                user_id = request.GET.get('userId')
                if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                    offset = int(request.GET.get('offset'))
                    limit = offset + int(request.GET.get('limit'))
                    if user_id is None:
                        likes = MgtLikesInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()[offset:limit]
                    else:
                        likes = MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()[offset:limit]
                else:
                    if user_id is None:
                        likes = MgtLikesInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()
                    else:
                        likes = MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()
                json_params = {}
                json_params['likes'] = []
                for like in likes:
                    json_param = {
                        "id": str(like.id),
                        "userId": like.user_id,
                        "postId": like.post_id,
                        "createdAt": str(like.created_at),
                        "updatedAt": str(like.updated_at)
                    }
                    json_params['likes'].append(json_param)
                json_params['total'] = len(json_params['likes'])
                status = 200
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
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # いいね登録
    def post(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            user_id = request.GET.get('userId')
            if not MgtPostsInfo.objects.filter(post_id=post_id).exists():
                json_params = {
                    "message": "post not exist"
                }
                status = 404
            elif not MgtUsersInfo.objects.filter(user_id=user_id).exists():
                json_params = {
                    "message": "user not exist"
                }
                status = 404
            else:
                if not MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).exists():
                    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                    dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                    MgtLikesInfo.objects.create(user_id=user_id, post_id=post_id, created_at=dt_now, updated_at=dt_now)
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

    # いいね削除
    def delete(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            user_id = request.GET.get('userId')
            if not MgtPostsInfo.objects.filter(post_id=post_id).exists():
                json_params = {
                    "message": "post not exist"
                }
                status = 404
            elif not MgtUsersInfo.objects.filter(user_id=user_id).exists():
                json_params = {
                    "message": "user not exist"
                }
                status = 404
            else:
                if MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).exists():
                    like = MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id))
                    like.delete()
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

# /posts/postId/comments
class Comments(TemplateView):

    # コメント取得
    def get(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if not MgtPostsInfo.objects.filter(post_id=post_id).exists():
                json_params = {
                    "message": "post not exist"
                }
                status = 404
            else:
                user_id = request.GET.get('userId')
                if request.GET.get('offset') is not None and request.GET.get('limit') is not None:
                    offset = int(request.GET.get('offset'))
                    limit = offset + int(request.GET.get('limit'))
                    if user_id is None:
                        comments = MgtCommentsInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()[offset:limit]
                    else:
                        comments = MgtCommentsInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()[offset:limit]
                else:
                    if user_id is None:
                        comments = MgtCommentsInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()
                    else:
                        comments = MgtCommentsInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()
                json_params = {}
                json_params['comments'] = []
                for comment in comments:
                    json_param = {
                        "id": str(comment.id),
                        "userId": comment.user_id,
                        "postId": comment.post_id,
                        "comment": comment.comment,
                        "createdAt": str(comment.created_at),
                        "updatedAt": str(comment.updated_at)
                    }
                    json_params['comments'].append(json_param)
                json_params['total'] = len(json_params['comments'])
                status = 200
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status)

    # コメント登録
    def post(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            user_id = request.GET.get('userId')
            data = json.loads(request.body)
            comment = data['comment']
            if not MgtPostsInfo.objects.filter(post_id=post_id).exists():
                json_params = {
                    "message": "post not exist"
                }
                status = 404
            elif not MgtUsersInfo.objects.filter(user_id=user_id).exists():
                json_params = {
                    "message": "user not exist"
                }
                status = 404
            else:
                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                MgtCommentsInfo.objects.create(user_id=user_id, post_id=post_id, comment=comment, created_at=dt_now, updated_at=dt_now)
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

    # コメント削除
    def delete(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            user_id = request.GET.get('userId')
            if not MgtPostsInfo.objects.filter(post_id=post_id).exists():
                json_params = {
                    "message": "post not exist"
                }
                status = 404
            else:
                comment = MgtCommentsInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id))
                comment.delete()
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