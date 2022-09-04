from django.db import models

class MgtUsersInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    bone_type = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.TextField(blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mgt_users_info'