from django.db import models
from general.models import BaseModel
from question.models import Options
from student.models import  StudentRecord
from django.db.models.signals import post_save
from django.dispatch import receiver

class University(BaseModel):
    service=models.ForeignKey('service.ServiceType',on_delete=models.CASCADE,blank=True,null=True)
    country=models.ManyToManyField('Country')
    state=models.ManyToManyField('States')
    university_logo=models.ImageField(upload_to='Images',blank=True,null=True)
    university_image=models.ImageField(upload_to='Images',blank=True,null=True)
    university_name=models.CharField(max_length=300,blank=True,null=True)
    about_university=models.TextField(blank=True,null=True)
    sample_certificate=models.ImageField(upload_to='Images',blank=True,null=True)
    prospectus=models.FileField(upload_to='Files',blank=True,null=True)
    options=models.ManyToManyField('question.Options')
    approved_by=models.ManyToManyField('course.Accreditation')
    student_choice=models.CharField(max_length=200,blank=True,null=True)
    student_review=models.CharField(max_length=200,blank=True,null=True)
    credit_points=models.CharField(max_length=200,blank=True,null=True)
    e_learning_facility=models.CharField(max_length=300,blank=True,null=True)
    placement_assistance=models.CharField(max_length=200,blank=True,null=True)
    industry_ready=models.CharField(max_length=200,blank=True,null=True)
    satisfied_student=models.CharField(max_length=200,blank=True,null=True)
    pros=models.TextField(blank=True,null=True)
    world_ranking=models.CharField(max_length=200,blank=True,null=True)
    country_ranking=models.CharField(max_length=200,blank=True,null=True)
    nirf_training=models.CharField(max_length=200,blank=True,null=True)
    wes_approval=models.CharField(max_length=200,blank=True,null=True)
    rating=models.CharField(blank=True,null=True)
    highlight_text = models.CharField(max_length=255,null=True,blank=True)
    highlight_color = models.CharField(max_length=100,null=True,blank=True)
    slug=models.TextField(default="")

    class Meta:
        db_table='University'
    
    def __str__(self):
        return self.university_name

class FacilityType(BaseModel):
    facility=models.CharField(max_length=500,blank=True,null=True)
    class Meta:
        db_table='FacilityType'
    def __str__(self):
        return self.facility
    
class Facilities(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    facility=models.ForeignKey('course.FacilityType',on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=500,blank=True,null=True)
    image=models.ImageField(upload_to='Images',blank=True,null=True)
    distance=models.CharField(max_length=500,blank=True,null=True)
    fee=models.CharField(max_length=500,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Facilities'
    def __str__(self):
        return self.name


class Facts(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    facts=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Facts'
    def __str__(self):
        return self.facts


class UniversityImages(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to='Images',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='UniversityImages'
    

class Accreditation(models.Model):
    approved_by=models.CharField(max_length=500,blank=True,null=True)
    name=models.CharField(max_length=500,blank=True,null=True)
    logo=models.ImageField(upload_to='Images',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Accreditation'

class AccreditationPoints(models.Model):
    approval=models.ForeignKey('course.Accreditation',on_delete=models.CASCADE,blank=True,null=True)
    points=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='AccreditationPoints'

class Course(BaseModel):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    course_type=models.ForeignKey('service.CourseType',on_delete=models.CASCADE,blank=True,null=True)
    # specialization=models.ManyToManyField('Specialization')
    course_name=models.CharField(max_length=200,blank=True,null=True)
    icon=models.ImageField(upload_to='Images',blank=True,null=True)
    duration=models.CharField(max_length=200,blank=True,null=True)
    duration_description=models.TextField(blank=True,null=True)
    course_image=models.ImageField(upload_to='Images',blank=True,null=True)
    course_details=models.TextField(blank=True,null=True)
    video=models.FileField(upload_to='Files',blank=True,null=True)
    audio=models.FileField(upload_to='Files',blank=True,null=True)
    eligibility=models.CharField(max_length=200,blank=True,null=True)
    eligibility_description=models.TextField(blank=True,null=True)
    admission_procedure=models.TextField(blank=True,null=True)
    semester_fee=models.CharField(max_length=300,blank=True,null=True)
    converted_sem_fee=models.CharField(max_length=200,blank=True,null=True)
    year_fee=models.CharField(max_length=500,blank=True,null=True)
    converted_year_fee=models.CharField(max_length=200,blank=True,null=True)
    full_fee=models.CharField(max_length=300,blank=True,null=True)
    converted_full_fee=models.CharField(max_length=200,blank=True,null=True)
    fees_description=models.TextField(blank=True,null=True)
    syllabus=models.FileField(upload_to='Files',blank=True,null=True)
    type=models.CharField(max_length=200,default=" ",blank=True,null=True)
    currency = models.ForeignKey('course.CurrencySymbol',null=True,blank=True,on_delete=models.CASCADE)
    slug=models.TextField(default="")

    class Meta:
        db_table='Course'
    
    def __str__(self):
        return self.course_name
    
class AdmissionProcedures(models.Model):
    course=models.ForeignKey('course.Course',on_delete=models.CASCADE,blank=True,null=True)
    specialization=models.ForeignKey('course.Specialization',on_delete=models.CASCADE,blank=True,null=True)
    points=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='AdmissionProcedures'
    

class CourseSpecialization(models.Model):
    course=models.ForeignKey('course.Course',on_delete=models.CASCADE,blank=True,null=True)
    specialization=models.CharField(max_length=300,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='CourseSpecialization'
    
    def __str__(self):
        return self.specialization

# class Specialization(models.Model):
#     specialization_name=models.CharField(max_length=500,blank=True,null=True)
#     is_deleted=models.BooleanField(default=False)
 
#     class Meta:
#         db_table='Specialization'
#     def __str__(self):
#         return str(self.specialization_name)

class Country(models.Model):
    country=models.CharField(max_length=200,blank=True,null=True)
    flag=models.ImageField(upload_to='Images',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Country'
    
    def __str__(self):
        return self.country

class Faq(models.Model):
    course=models.ForeignKey('course.Course',on_delete=models.CASCADE,blank=True,null=True)
    specialization=models.ForeignKey('course.Specialization',on_delete=models.CASCADE,blank=True,null=True)
    faq_question=models.TextField(blank=True,null=True)
    faq_answer=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Faq'
    
    def __str__(self):
        return self.faq_question



class UniversityBanner(models.Model):
    banner=models.ImageField(upload_to='Images',blank=True,null=True)
    banner_url=models.URLField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='UniversityBanner'
  
    
    
class PlacementPartners(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    placement_partner_name=models.CharField(max_length=300,blank=True,null=True)
    placement_partner_logo=models.ImageField(upload_to='Images',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='PlacementPartners'
   
class CurrencySymbol(models.Model):
    symbol=models.CharField(max_length=200,blank=True,null=True)
    symbol_name=models.CharField(max_length=300,blank=True,null=True)
    source_currency=models.CharField(default="USD",max_length=200,blank=True,null=True)
    order_id=models.PositiveIntegerField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    
    class Meta:
        db_table='CurrencySymbol'

    def __str__(self) -> str:
        return self.symbol if self.symbol else self.id
def set_order_id(sender, instance, **kwargs):
        if not instance.order_id:
            
            max_order_id = CurrencySymbol.objects.filter(is_deleted=False).aggregate(models.Max('order_id'))['order_id__max']
            instance.order_id = max_order_id + 1 if max_order_id is not None else 1

            instance.save()


post_save.connect(set_order_id, sender=CurrencySymbol)

    
class Specialization(BaseModel):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    course=models.ForeignKey('course.Course',on_delete=models.CASCADE,blank=True,null=True)
    specialization_name=models.CharField(max_length=300,blank=True,null=True)
    duration=models.CharField(max_length=200,blank=True,null=True)
    duration_description=models.TextField(blank=True,null=True)
    specialization_image=models.ImageField(upload_to='Images',blank=True,null=True)
    specialization_details=models.TextField(blank=True,null=True)
    video=models.FileField(upload_to='Files',blank=True,null=True)
    audio=models.FileField(upload_to='Files',blank=True,null=True)
    eligibility=models.CharField(max_length=200,blank=True,null=True)
    eligibility_description=models.TextField(blank=True,null=True)
    admission_procedure=models.TextField(blank=True,null=True)
    semester_fee=models.CharField(max_length=300,blank=True,null=True)
    converted_sem_fee=models.CharField(max_length=200,blank=True,null=True)
    year_fee=models.PositiveIntegerField(blank=True,null=True)
    converted_year_fee=models.CharField(max_length=200,blank=True,null=True)
    full_fee=models.CharField(max_length=300,blank=True,null=True)
    converted_full_fee=models.CharField(max_length=200,blank=True,null=True)
    fees_description=models.TextField(blank=True,null=True)
    currency = models.ForeignKey('course.CurrencySymbol',null=True,blank=True,on_delete=models.CASCADE)
    syllabus=models.FileField(upload_to='Files',blank=True,null=True)
    slug=models.TextField(default="")

    class Meta:
        db_table='Specialization'
    
    def __str__(self):
        return self.specialization_name
         

class UniversityDocuments(models.Model):
    student=models.ForeignKey('student.StudentRecord',on_delete=models.CASCADE,blank=True,null=True)
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    document_name=models.CharField(max_length=500,blank=True,null=True)
    document=models.FileField(upload_to='Files',blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='UniversityDocuments'
        

class States(models.Model):
    country=models.ForeignKey('course.Country',on_delete=models.CASCADE,blank=True,null=True)
    state_name=models.CharField(max_length=500,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='States'

class AlumniTalk(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    review=models.TextField(blank=True,null=True)
    rating=models.CharField(max_length=200,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='AlumniTalk'

# Create your models here.