from django.contrib import admin
from student.models import RecordAnswer,StudentRecord,StudentWishList,StudentProfile,Enquiry,ReviewStudent,CollageSuggestion

class RecordAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'userid','option']
admin.site.register(RecordAnswer, RecordAnswerAdmin)


class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'university', 'grade_10_certificate', 'grade_12_certificate', 'degree_certificate', 'passport', 'visa', 'personal_id', 'status','is_read','notification')

admin.site.register(StudentRecord, StudentRecordAdmin)

class ReviewStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'university','rating','review')

admin.site.register(ReviewStudent, ReviewStudentAdmin)


class StudentWishListAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'university','course','is_active')

admin.site.register(StudentWishList, StudentWishListAdmin)

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email','mobile','gender','dob','country_code','status')

admin.site.register(StudentProfile, StudentProfileAdmin)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name','email','phone','message','is_read')

admin.site.register(Enquiry, EnquiryAdmin)

admin.site.register(CollageSuggestion)
# Register your models here.
