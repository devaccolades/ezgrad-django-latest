from django.db import models
from django.contrib.auth.models import User,Group
from general.models import BaseModel
from decouple import config

STATUS_CHOICES = (
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),

)

REGISTER_STATUS_CHOICES=(
    ('pending','Pending'),
    ('follow up','Follow Up'),
    ('converted','Converted'),
    ('not interested','Not Interested'),
)

class StudentProfile(BaseModel):

    name=models.CharField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    country_code=models.CharField(max_length=500,blank=True,null=True)
    # phone_number_length=models.IntegerField(blank=True,null=True)
    mobile=models.BigIntegerField(blank=True,null=True)
    gender=models.CharField(max_length=100,blank=True,null=True)
    dob=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=200,choices=REGISTER_STATUS_CHOICES,default="pending")
    username = models.CharField(max_length=128, blank=True, null=True)
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    register_date=models.DateTimeField(auto_now_add=True)
    course = models.CharField(max_length=300,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:

        db_table="StudentProfile"
        ordering = ('-register_date',)

    def __str__(self):
        return self.username if self.username else self.email

class ReviewStudent(models.Model):
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    rating=models.IntegerField(blank=True,null=True)
    review=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table="ReviewStudent"


class RecordAnswer(models.Model):
    option=models.ForeignKey('question.Options',on_delete=models.CASCADE,blank=True,null=True)
    userid=models.ForeignKey('student.StudentProfile',on_delete=models.CASCADE,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='RecordAnswer'

class StudentRecord(models.Model):
    student=models.ForeignKey('student.StudentProfile',on_delete=models.CASCADE,blank=True,null=True)
    course=models.ForeignKey('course.Course',on_delete=models.CASCADE,blank=True,null=True)
    university=models.ForeignKey('course.University',on_delete=models.CASCADE,blank=True,null=True)
    grade_10_certificate=models.FileField(upload_to='Files',blank=True,null=True)
    grade_12_certificate=models.FileField(upload_to='Files',blank=True,null=True)
    degree_certificate=models.FileField(upload_to='Files',blank=True,null=True)
    passport=models.FileField(upload_to='Files',blank=True,null=True)
    visa=models.FileField(upload_to='Files',blank=True,null=True)
    personal_id=models.FileField(upload_to='Files',blank=True,null=True)
    status=models.CharField(max_length=200,choices=STATUS_CHOICES,default='pending')
    is_read=models.BooleanField(default=False)
    notification=models.BooleanField(default=False)
    application_date=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='StudentRecord'
        verbose_name = ('Student Record')
        verbose_name_plural = ('Student Records')
        ordering = ('-application_date',)
    def __str__(self):
        return self.student.name

class StudentWishList(BaseModel):
    student = models.ForeignKey('student.StudentProfile',on_delete=models.CASCADE, blank=True,null=True)
    university = models.ForeignKey('course.University',on_delete=models.CASCADE, blank=True,null=True)
    course = models.ForeignKey('course.Course',on_delete=models.CASCADE, blank=True,null=True)
    is_active=models.BooleanField(default=False)

    class Meta:
        db_table = 'student_student_wishlist'
        verbose_name = ('Student Wishlist')
        verbose_name_plural = ('Student Wishlists')
        ordering = ('id',)

    def __str__(self):
        return f'{self.student.name}-{self.university.university_name}'



class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    class Meta:
        db_table='CustomUser'

    
class Enquiry(models.Model):
    enquiry_date=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=200,blank=True,null=True)
    last_name=models.CharField(max_length=200,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    phone=models.BigIntegerField(blank=True,null=True)
    message=models.TextField(blank=True,null=True)
    is_read=models.BooleanField(default=False)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Enquiry'
        ordering = ('-enquiry_date',)
    
    def __str__(self):
        return str(self.enquiry_date)


class CollageSuggestion(BaseModel):
    service=models.ManyToManyField('service.ServiceType')
    university = models.ManyToManyField('course.University')
    profile_image=models.ImageField(upload_to='Images',blank=True,null=True)
    full_name= models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255,null=True,blank=True)
    mobile=models.BigIntegerField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    redirect_link = models.TextField(blank=True,null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.redirect_link = f'{config("main_url")}/suggested-collage/{self.id}'
        super().save(update_fields=['redirect_link'])

    def __str__(self):
        return self.full_name if self.full_name else self.id