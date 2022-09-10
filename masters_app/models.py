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