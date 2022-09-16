from django.db import models

class MgtPostsInfo(models.Model):
    post_id = models.CharField(primary_key=True, max_length=255)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    size = models.ForeignKey('MgtSizeList', models.DO_NOTHING, blank=True, null=True)
    color = models.ForeignKey('MgtColorList', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey('MgtCategoryList', models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey('MgtBrandList', models.DO_NOTHING, blank=True, null=True)
    video = models.TextField()
    thumbnail = models.TextField()
    sample_image = models.TextField(blank=True, null=True)
    page_url = models.TextField(blank=True, null=True)
    user_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_posts_info'

class MgtSizeList(models.Model):
    size_id = models.IntegerField(primary_key=True)
    size = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_size_list'

class MgtColorList(models.Model):
    color_id = models.IntegerField(primary_key=True)
    color = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_color_list'

class MgtCategoryList(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_category_list'

class MgtBrandList(models.Model):
    brand_id = models.IntegerField(primary_key=True)
    brand = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_brand_list'

class MgtUsersInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.ForeignKey('MgtGenderList', models.DO_NOTHING, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    bone_type = models.ForeignKey('MgtBoneTypeList', models.DO_NOTHING, blank=True, null=True)
    profile_pic = models.TextField(blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_users_info'

class MgtGenderList(models.Model):
    gender_id = models.IntegerField(primary_key=True)
    gender = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_gender_list'
    
class MgtBoneTypeList(models.Model):
    bone_type_id = models.IntegerField(primary_key=True)
    bone_type = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_bone_type_list'
