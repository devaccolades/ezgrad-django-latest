from django.contrib import admin
from web.models import Contact,Details,Experts,Subbanner,MainBanner,PlacedStudent,Checklist,Blogs,Tags,Category,Careers,CareerApply,BlogComment,BlogReplyComment

class MainBannerAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'main_banner',
        'main_banner_url',
        
    ]
admin.site.register(MainBanner,MainBannerAdmin)


class SubbannerAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'sub_banner',
        'title',
        'content',
    ]
admin.site.register(Subbanner,SubbannerAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display=[
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
    ]
admin.site.register(Contact,ContactAdmin)


class DetailsAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'image',
        'title',
        'content',
        
    ]
admin.site.register(Details,DetailsAdmin)


class ExpertsAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'name',
        'role',
        'experience',
        'photo',
        'rating',
        'counselling',
       
    ]
admin.site.register(Experts,ExpertsAdmin)


class StudentTestimonialAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'image',
        'name',
        'graduated_university',
        'year',
        'placed_organisation',
        'testimonial',
    ]
admin.site.register(PlacedStudent,StudentTestimonialAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'title',
        'description',
        'image',
        'video',
        'slug',
        'featured',
        'blog_date',
    ]
admin.site.register(Blogs,BlogAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Tags, TagsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Category, CategoryAdmin)


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'comment', 'name', 'email','phone','is_active')

admin.site.register(BlogComment, BlogCommentAdmin)


class BlogReplyCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_comment', 'reply_comment')

admin.site.register(BlogReplyComment, BlogReplyCommentAdmin)


class CareerAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'job_description','job_mode','job_type','date_added')

admin.site.register(Careers, CareerAdmin)


class CareerApplyAdmin(admin.ModelAdmin):
    list_display=('id','name','email','phone','apply_for','cv','date_applied')

admin.site.register(CareerApply,CareerApplyAdmin)

class ChecklistAdmin(admin.ModelAdmin):
    
    list_display=('id','title','description')

admin.site.register(Checklist,ChecklistAdmin)


# Register your models here.

