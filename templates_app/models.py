from django.db import models

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

class MgtTemplatesInfo(models.Model):
    template_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('MgtUsersInfo', models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_templates_info'