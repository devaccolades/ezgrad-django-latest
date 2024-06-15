from django.db import models
from general.models import BaseModel

class ServiceType(BaseModel):
    service=models.CharField(max_length=300,blank=True,null=True)
    class Meta:
        db_table='ServiceType'
        verbose_name = 'ServiceType'
        verbose_name_plural = 'ServiceTypes'
        ordering = ('id',)

    def __str__(self):
        return self.service

    
class CourseType(models.Model):
    service=models.ForeignKey('service.ServiceType', on_delete=models.CASCADE, blank=True, null=True)
    course_type=models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=False)
    
    
    class Meta:
        db_table='CourseType'

    def __str__(self):
        return self.course_type
        
# Create your models here.
