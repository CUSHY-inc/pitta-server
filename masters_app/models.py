from django.db import models

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