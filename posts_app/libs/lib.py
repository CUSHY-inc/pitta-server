from django.conf import settings
import boto3
import re

# コンテンツDL用 URL作成
def create_url(path):
    if path is not None:
        if len(str(path)) != 0:
            try:
                s3_client = boto3.client('s3')
                BUCKET = settings.PITTA_ENV
                OBJECT = path
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET, 'Key': OBJECT},
                    ExpiresIn=300)
                return url
            except:
                return None
    else:
        return None

# キャメルケースからスネークケースへの変換
def conversion_from_camel_to_snake(str):
    return re.sub("([A-Z])",lambda x:"_" + x.group(1).lower(),str)