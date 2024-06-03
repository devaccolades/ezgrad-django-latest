from django.db import models

class Questions(models.Model):
    service=models.ForeignKey('service.ServiceType',on_delete=models.CASCADE,blank=True,null=True)
    question=models.CharField(max_length=500,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Questions'
        

    def __str__(self):
        return self.question

class Options(models.Model):
    question=models.ForeignKey('question.Questions', on_delete=models.CASCADE, blank=True, null=True)
    options=models.CharField(max_length=300,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Options'

    def __str__(self):
        return self.options


    
# Create your models here.

