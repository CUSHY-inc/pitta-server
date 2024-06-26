from wsgiref import headers
from django.conf import settings
from botocore.client import Config
import boto3
import re
import base64
import magic
import os
import glob
import mimetypes

######### クラス定義 #########

# offset/limitクラス
class OffsetLimit:
    def __init__(self,offset,limit):
        if offset is not None:
            self.offset = int(offset)
        else:
            self.offset = 0
        if limit is not None:
            self.limit = self.offset + int(limit)
        else:
            self.limit = self.offset + 10

######### 関数定義 #########

# S3 DL用 URL作成
def create_url(path):
    if path is not None:
        if len(str(path)) != 0:
            try:
                s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
                BUCKET = settings.PITTA_ENV
                OBJECT = path
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET, 'Key': OBJECT},
                    ExpiresIn=604800
                    )
                return url
            except:
                return None
    else:
        return None

# キャメルケースからスネークケースへの変換
def conversion_from_camel_to_snake(str):
    return re.sub("([A-Z])",lambda x:"_" + x.group(1).lower(),str)

# Base64のファイルをデコードして指定のS3フォルダに格納
def decode_and_storage(file_data, s3_path, file_name):
    file = base64.b64decode(file_data)
    file_type = magic.from_buffer(file, mime=True)
    extension = re.findall('^.*/(.*)$', file_type)[0]
    with open('/mnt/goofys/{0}/{1}.{2}'.format(s3_path, file_name, extension), 'wb') as f:
        f.write(file)
    s3_client = boto3.client('s3')
    FILE = '/mnt/goofys/{0}/{1}.{2}'.format(s3_path, file_name, extension)
    BUCKET = settings.PITTA_ENV
    KEY = '{0}/{1}.{2}'.format(s3_path, file_name, extension)
    CONTENT_TYPE = mimetypes.guess_type(FILE)[0]
    s3_client.upload_file(FILE, BUCKET, KEY, ExtraArgs={"ContentType": CONTENT_TYPE})

    return '{0}/{1}.{2}'.format(s3_path, file_name, extension)

# ファイル削除
def delete_file(s3_path, regexp):
    for file_name in glob.glob('/mnt/goofys/{0}/{1}*'.format(s3_path, regexp)):
        os.remove(file_name)
