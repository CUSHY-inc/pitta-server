from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import MgtPostsInfo, MgtUsersInfo, MgtCommentsInfo
from django.db.models import Q
import datetime
import json
import uuid
import traceback

# /comments
class Comments(TemplateView):

    # コメント登録
    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
            user_id = data['userId']
            post_id = data['postId']
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
                comment = MgtCommentsInfo.objects.create(user_id=user_id, post_id=post_id, comment=comment, created_at=dt_now, updated_at=dt_now)
                json_params = {
                    "commentId": str(comment.comment_id),
                    "userId": str(comment.user_id),
                    "postId": str(comment.post_id),
                    "comment": comment.comment,
                    "createdAt": str(comment.created_at),
                    "updatedAt": str(comment.updated_at)
                }
                status = 200
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

# /comments/commentId
class CommentId(TemplateView):

    # コメント削除
    def delete(self, request, **kwargs):
        try:
            comment_id = kwargs['parameter']
            if not MgtCommentsInfo.objects.filter(comment_id=comment_id).exists():
                json_params = {
                    "message": "comment not exist"
                }
                status = 404
            else:
                comment = MgtCommentsInfo.objects.get(comment_id=comment_id)
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