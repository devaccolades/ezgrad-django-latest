from rest_framework import serializers
from dateutil import parser
from web.models import *

class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model= MainBanner
        fields=(
            'id',
            'main_banner',
            'main_banner_url',
            'content',
        )

class AddMainBannerSerializer(serializers.Serializer):
    main_banner=serializers.FileField()
    main_banner_url=serializers.URLField()
    content=serializers.CharField()

class SubbannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subbanner
        fields=(
            'id',
            'sub_banner',
            'title',
            'content',
        )
class AddSubBannerSerializer(serializers.Serializer):
    sub_banner=serializers.FileField()
    title=serializers.CharField()
    content=serializers.CharField()

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=(
            'id',
            'about',
            'address',
            'phone',
            'email',
            'facebook_url',
            'instagram_url',
            'youtube_url',
            'whatsapp_url',
            'linkedln_url',
        )
class AddContactSerializer(serializers.Serializer):
    about=serializers.CharField()
    address=serializers.CharField()
    phone=serializers.IntegerField()
    email=serializers.CharField()
    facebook_url=serializers.CharField()
    instagram_url=serializers.CharField()
    youtube_url=serializers.CharField()
    whatsapp_url=serializers.IntegerField()
    linkedln_url=serializers.CharField()


class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Details
        fields=(
            'id',
            'image',
            'title',
            'content',
        )

class AddDetailSerializer(serializers.Serializer):
    image=serializers.FileField()
    title=serializers.CharField()
    content=serializers.CharField()


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model=Experts
        fields=(
            'id',
            'name',
            'role', 
            'experience',
            'photo',
            'rating',
            'counselling',
        )

class AddExpertSerializer(serializers.Serializer):
    name=serializers.CharField()
    role=serializers.CharField()
    experience=serializers.CharField()
    photo=serializers.FileField()
    rating=serializers.IntegerField()
    counselling=serializers.IntegerField()


class PlacedStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacedStudent
        fields = ['id','image','name','graduated_university','year','placed_organisation','testimonial']
# class AddStudentTestimonialSerializer(serializers.Serializer):
#     image=serializers.ImageField()
#     university=serializers.CharField()

# class StudentTestimonialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=StudentTestimonials
#         fields=(
#             'id',
#             'image',
#             'university',
#         )


class CreateBlogSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    # image = serializers.FileField()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tags
        fields=(
            'id',
            'name'
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Tags
        fields=(
            'id',
            'name'
        )

            

class ListBlogSerializer(serializers.ModelSerializer):
    tags=serializers.SerializerMethodField()
    category=serializers.SerializerMethodField()
    blog_date=serializers.SerializerMethodField()
    class Meta:
        model = Blogs
        fields = (
            'id',
            'slug',
            'title',
            'blog_date',
            'description',
            'image',
            'video',
            'category',
            'tags',
            'featured',
            )
    def get_blog_date(self,instance):
        if instance.blog_date:
            date = instance.blog_date
            formatted_date = date.strftime("%A, %B %d, %Y")
            date_obj = parser.parse(formatted_date)
            day = date_obj.day
            year = date_obj.year
            month = date_obj.strftime("%b")
            date = f"{month} {day} {year}"
            return date
    def get_tags(self,instance):
        request = self.context["request"]
        if instance.tags:
            selected_tags=instance.tags.all()
            serialized_data = TagSerializer(
                    selected_tags,
                    context = {
                        "request" : request
                    },
                    many=True
                ).data

            return serialized_data
        else:
            return None

    def get_category(self,instance):
        request = self.context["request"]
        if instance.category:
            selected_category=instance.category.all()
            serialized_data = CategorySerializer(
                    selected_category,
                    context = {
                        "request" : request
                    },
                    many=True
                ).data

            return serialized_data
        else:
            return None




class CreateCommentSerializer(serializers.Serializer):
    comment = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()


class ListCommentSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        fields = (
            'id',
            'comment',
            'date_added',
            'name',
            'email',
            'phone',
        )

    def get_date_added(self, instance):
        if instance.date_added:
            date = instance.date_added
            formatted_date = date.strftime("%A, %B %d, %Y")
            date_obj = parser.parse(formatted_date)
            day = date_obj.day
            year = date_obj.year
            month = date_obj.strftime("%b")
            date = f"{month} {day} {year}"
            return date
        

class AddCareerSerializer(serializers.Serializer):
    job_title=serializers.CharField()
    job_description=serializers.CharField()
    job_mode=serializers.CharField()
    job_type=serializers.CharField()

class CareerSerializer(serializers.ModelSerializer):
    date_added=serializers.SerializerMethodField()
    class Meta:
        model=Careers
        fields=(
            'id',
            'job_title',
            'job_description',
            'description',
            'job_mode',
            'job_type',
            'date_added',
            'hiring',
        )
    def get_date_added(self, instance):
        if instance.date_added:
            date = instance.date_added
            formatted_date = date.strftime("%A, %B %d, %Y")
            date_obj = parser.parse(formatted_date)
            day = date_obj.day
            year = date_obj.year
            month = date_obj.strftime("%b")
            date = f"{month} {day} {year}"
            return date
        
class AddCareerApplySerializer(serializers.Serializer):
    name=serializers.CharField()
    phone=serializers.IntegerField()
    
class CareerApplySerializer(serializers.ModelSerializer):
    date_applied=serializers.SerializerMethodField()
    apply_job=serializers.SerializerMethodField()
    class Meta:
        model=CareerApply
        fields=(
            'id',
            'name',
            'email',
            'phone',
            'cv',
            'apply_for',
            'apply_job',
            'date_applied',
        )
    def get_date_applied(self, instance):
        if instance.date_applied:
            date = instance.date_applied
            formatted_date = date.strftime("%A, %B %d, %Y")
            date_obj = parser.parse(formatted_date)
            day = date_obj.day
            year = date_obj.year
            month = date_obj.strftime("%b")
            date = f"{month} {day} {year}"
            return date
    def get_apply_job(self,instance):
        if instance.apply_for:
            return instance.apply_for.job_title
        else:
            return None
        

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model= Checklist
        fields=(
            'id',
            'title',
            'description',
        )

# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Careers
#         fields = '__all__'