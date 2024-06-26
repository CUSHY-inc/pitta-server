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
            ofs_lim = lib.OffsetLimit(request.GET.get('offset'), request.GET.get('limit'))
            posts = MgtPostsInfo.objects.all().order_by('created_at').reverse()[ofs_lim.offset:ofs_lim.limit]
            json_params = []
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
                    "video": None,
                    "thumbnailUrl": lib.create_url(post.thumbnail),
                    "thumbnail": None,
                    "sampleImageUrl": post.sample_image_url,
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
        except:
            json_params = {
                "message": traceback.format_exc()
            }
            status = 400
        finally:
            json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
            return HttpResponse(json_str, status=status, content_type="application/json")

    # 新規投稿
    def post(self,request):
        try:
            data = json.loads(request.body)
            user_id = data['user']['userId']
            post_id = uuid.uuid4()

            if MgtUsersInfo.objects.filter(user_id=user_id).exists():

                # base64で送られてきたデータをデコードしてS3に格納
                if data['video'] is not None:
                    video = lib.decode_and_storage(data['video'], 'videos/posts', post_id)
                else:
                    video = None
                if data['thumbnail'] is not None:
                    thumbnail = lib.decode_and_storage(data['thumbnail'], 'pictures/thumbnails', post_id)
                else:
                    thumbnail = None

                dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
                dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
                post = MgtPostsInfo.objects.create(post_id=post_id, item_id=data['itemId'], item_name=data['itemName'], size_id=data['sizeId'], color_id=data['colorId'], category_id=data['categoryId'], description=data['description'], brand_id=data['brandId'], video=video, thumbnail=thumbnail, sample_image_url=data['sampleImageUrl'], page_url=data['pageUrl'], user_id=user_id, created_at=dt_now, updated_at=dt_now)
                user = MgtUsersInfo.objects.get(user_id=user_id)
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
                    "video": None,
                    "thumbnailUrl": lib.create_url(post.thumbnail),
                    "thumbnail": None,
                    "sampleImageUrl": post.sample_image_url,
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
                        "profilePicUrl": lib.create_url(user.profile_pic),
                        "profilePic": None,
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
                    "video": None,
                    "thumbnailUrl": lib.create_url(post.thumbnail),
                    "thumbnail": None,
                    "sampleImageUrl": post.sample_image_url,
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
                        "profilePicUrl": lib.create_url(user.profile_pic),
                        "profilePic": None,
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
            return HttpResponse(json_str, status=status, content_type="application/json")

    # 投稿削除
    def delete(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                post = MgtPostsInfo.objects.get(post_id=post_id)
                post.delete()
                lib.delete_file('pictures/thumbnails', post_id)
                lib.delete_file('videos/posts', post_id)
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
                return HttpResponse(status=status, content_type="application/json")
            else:
                json_str = json.dumps(json_params, ensure_ascii=False, indent=2)
                return HttpResponse(json_str, status=status, content_type="application/json")

# /posts/postId/likes
class Likes(TemplateView):

    # いいね一覧取得
    def get(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                ofs_lim = lib.OffsetLimit(request.GET.get('offset'), request.GET.get('limit'))
                user_id = request.GET.get('userId')
                if user_id is None:
                    likes = MgtLikesInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()[ofs_lim.offset:ofs_lim.limit]
                else:
                    likes = MgtLikesInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()[ofs_lim.offset:ofs_lim.limit]
                json_params = {
                    "totalLikes": MgtLikesInfo.objects.filter(post_id=post_id).count(),
                    "likes": []
                }
                for like in likes:
                    json_param = {
                        "likeId": str(like.like_id),
                        "userId": str(like.user_id),
                        "postId": str(like.post_id),
                        "createdAt": str(like.created_at),
                        "updatedAt": str(like.updated_at)
                    }
                    json_params['likes'].append(json_param)
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
            return HttpResponse(json_str, status=status, content_type="application/json")

# /posts/postId/comments
class Comments(TemplateView):

    # コメント取得
    def get(self, request, **kwargs):
        try:
            post_id = kwargs['parameter']
            if MgtPostsInfo.objects.filter(post_id=post_id).exists():
                ofs_lim = lib.OffsetLimit(request.GET.get('offset'), request.GET.get('limit'))
                user_id = request.GET.get('userId')
                if user_id is None:
                    comments = MgtCommentsInfo.objects.filter(post_id=post_id).order_by('created_at').reverse()[ofs_lim.offset:ofs_lim.limit]
                else:
                    comments = MgtCommentsInfo.objects.filter(Q(post_id=post_id) & Q(user_id=user_id)).order_by('created_at').reverse()[ofs_lim.offset:ofs_lim.limit]
                json_params = {
                    "totalComments": MgtCommentsInfo.objects.filter(post_id=post_id).count(),
                    "comments": []
                }
                for comment in comments:
                    user = MgtUsersInfo.objects.get(user_id=comment.user_id)
                    json_param = {
                        "commentId": str(comment.comment_id),
                        "postId": str(comment.post_id),
                        "comment": comment.comment,
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
                        "createdAt": str(comment.created_at),
                        "updatedAt": str(comment.updated_at)
                    }
                    json_params['comments'].append(json_param)
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
            return HttpResponse(json_str, status=status, content_type="application/json")
