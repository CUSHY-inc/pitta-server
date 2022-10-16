from django.conf import settings
import boto3
import re
import base64
import magic
import os
import glob

# offset/limit初期値
offset = 0
limit = 10

# S3 DL用 URL作成
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

# Base64のファイルをデコードして指定のS3フォルダに格納
def decode_and_storage(file_data, s3_path, file_name):
    file = base64.b64decode(file_data)
    file_type = magic.from_buffer(file, mime=True)
    extension = re.findall('^.*/(.*)$', file_type)[0]
    with open('/mnt/goofys/{0}/{1}.{2}'.format(s3_path, file_name, extension), 'wb') as f:
        f.write(file)
    return '{0}/{1}.{2}'.format(s3_path, file_name, extension)

# ファイル削除
def delete_file(s3_path, regexp):
    for file_name in glob.glob('/mnt/goofys/{0}/{1}*'.format(s3_path, regexp)):
        os.remove(file_name)