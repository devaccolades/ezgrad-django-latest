from django.db import models
from ckeditor.fields import RichTextField
from general.models import BaseModel

class MainBanner(models.Model):
    main_banner=models.ImageField(upload_to='Images',blank=True,null=True)
    main_banner_url=models.URLField(blank=True,null=True)
    content=models.TextField(blank=True,null=True)
    status=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        db_table='MainBanner'



class Subbanner(models.Model):
    sub_banner=models.ImageField(upload_to='Images',blank=True,null=True)
    title=models.CharField(max_length=300,blank=True,null=True)
    content=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Subbanner'





class Contact(models.Model):
    about=models.TextField(blank=True,null=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    phone=models.BigIntegerField(blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    facebook_url=models.CharField(blank=True,null=True)
    instagram_url=models.CharField(blank=True,null=True)
    youtube_url=models.CharField(blank=True,null=True)
    whatsapp_url=models.BigIntegerField(blank=True,null=True) 
    linkedln_url=models.CharField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Contact'
    


class Details(models.Model):
    image=models.ImageField(upload_to='Images',blank=True,null=True)
    title=models.CharField(max_length=200,blank=True,null=True)
    content=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Details'
    
  

class Experts(models.Model):
    name=models.CharField(max_length=200,blank=True,null=True)
    role=models.CharField(max_length=200,blank=True,null=True)
    experience=models.CharField(max_length=200,blank=True,null=True)
    photo=models.ImageField(upload_to='Images',blank=True,null=True)
    rating=models.IntegerField(blank=True,null=True)
    counselling=models.IntegerField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Experts'
    
    

class StudentTestimonials(models.Model):
    image=models.ImageField(upload_to='Images',blank=True,null=True)
    university=models.CharField(max_length=300,blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='StudentTestimonials'
   

class Blogs(BaseModel):
    category=models.ManyToManyField("web.Category", blank=True)
    title = models.CharField(max_length=128)
    description = RichTextField()
    image = models.ImageField(upload_to='blogs/images', null=True, blank=True)
    video = models.FileField(upload_to='blogs/videos', null=True, blank=True)
    tags = models.ManyToManyField("web.Tags", blank=True)
    slug=models.TextField(default="")
    blog_date=models.DateField()
    featured=models.BooleanField(default=False)
    class Meta:
        db_table = 'Blogs'    
        verbose_name = ('Blog')
        verbose_name_plural = ('Blogs')
        ordering = ('blog_date',)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True)
    is_deleted=models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Category'
        verbose_name = ('category')
        verbose_name_plural = ('category')
    
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=125, null=True, blank=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        db_table = 'Tags'
        verbose_name = ('Tag')
        verbose_name_plural = ('Tags')

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    blog = models.ForeignKey("web.Blogs", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(null=True, blank=True, max_length=255)
    phone = models.BigIntegerField(blank=True,null=True)
    is_active = models.BooleanField(null=True, blank=True, default=False)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    is_deleted=models.BooleanField(default=False)

    class Meta:
        db_table = 'BlogComment'
        verbose_name = ('Blog Comment')
        verbose_name_plural = ('Blog Comments')

    def __str__(self):
        return self.comment


class BlogReplyComment(models.Model):
    blog_comment = models.ForeignKey("web.BlogComment", on_delete=models.CASCADE, null=True, blank=True)
    reply_comment = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    is_deleted=models.BooleanField(default=False) 

    class Meta:
        db_table = 'BlogReplyComment'
        verbose_name = ('Blog Reply Comment')
        verbose_name_plural = ('Blog Reply Comments')
        ordering = ('-date_added',)

class Careers(BaseModel):
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    job_title = models.CharField(max_length=255,blank=True,null=True)
    job_description = models.TextField(blank=True,null=True)
    description = RichTextField()
    job_mode = models.CharField(max_length=255,blank=True,null=True)
    job_type=models.CharField(max_length=255,blank=True,null=True)
    hiring=models.BooleanField(default=True)
    class Meta:
        db_table = 'Careers'
        verbose_name = ('Career')
        verbose_name_plural = ('Careers')
        ordering = ('-date_added',)


class CareerApply(BaseModel):
    date_applied=models.DateTimeField(db_index=True,auto_now_add=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    email=models.CharField(max_length=255,blank=True,null=True)
    phone=models.BigIntegerField(blank=True,null=True)
    cv=models.FileField(upload_to='Files',blank=True,null=True)
    apply_for=models.ForeignKey("web.Careers",on_delete=models.CASCADE,null=True,blank=True)
    class Meta:
        db_table='CareerApply'
        verbose_name = ('CareerApply')
        verbose_name_plural = ('CareerApply')
        ordering = ('-date_applied',)

class Checklist(models.Model):
    title=models.CharField(max_length=255,blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    class Meta:
        db_table='Checklist'














# Create your models here.



