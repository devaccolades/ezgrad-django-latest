from django.db import models
import uuid
from django.contrib.auth.models import User,Group


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted=models.BooleanField(default=False)
 
    class Meta:
        abstract = True
    
class ChiefProfile(BaseModel):
    username = models.CharField(max_length=128)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    password = models.TextField(blank=True, null=True)
    class Meta:
        db_table="ChiefProfile"

class Countries(models.Model):
    name=models.CharField(max_length=500,blank=True,null=True)
    web_code=models.CharField(max_length=500,blank=True,null=True)
    country_code=models.CharField(max_length=500,blank=True,null=True)
    flag=models.ImageField(upload_to='countries/flags',blank=True,null=True)
    phone_code=models.CharField(max_length=500,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    phone_number_length=models.IntegerField(blank=True,null=True)
    class Meta:
        db_table="Countries"
        

      






# Create your models here.

