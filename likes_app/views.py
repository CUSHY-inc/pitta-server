from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtPostsInfo, MgtUsersInfo, MgtLikesInfo
from django.conf import settings
from django.db.models import Q
import os
import datetime
import json
import traceback

# /likes
class Likes(TemplateView):

    # いいね登録
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data['userId']
            post_id = data['postId']
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
                    like = MgtLikesInfo.objects.create(user_id=user_id, post_id=post_id, created_at=dt_now, updated_at=dt_now)
                else:
                    like = MgtLikesInfo.objects.get(Q(user_id=user_id) & Q(post_id=post_id))
                json_params = {
                    "likeId": str(like.like_id),
                    "userId": str(like.user_id),
                    "postId": str(like.post_id),
                    "createdAt": str(like.created_at),
                    "updatedAt": str(like.updated_at)
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

# /likes/{likeId}
class LikeId(TemplateView):

    # いいね削除
    def delete(self, request, **kwargs):
        try:
            like_id = kwargs['parameter']
            if not MgtLikesInfo.objects.filter(like_id=like_id).exists():
                json_params = {
                    "message": "like not exist"
                }
                status = 404
            else:
                like = MgtLikesInfo.objects.get(like_id=like_id)
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
