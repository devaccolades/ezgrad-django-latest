from django.contrib import admin
from course.models import University,Facts,Facilities,AdmissionProcedures,UniversityImages,UniversityDocuments,AlumniTalk,States,AccreditationPoints,Specialization,Accreditation,FacilityType,Course,CurrencySymbol,CourseSpecialization,Country,Faq,UniversityBanner,PlacementPartners

class UniversityAdmin(admin.ModelAdmin):
    list_display=[
       'id',
       'service',
       'university_logo',
       'university_image',
       'university_name',
       'about_university',
       'sample_certificate',
       'prospectus',
       'student_choice',
       'student_review',
       'rating',
       'slug',
   
    ]
   
admin.site.register(University,UniversityAdmin)


class FacilitytypeAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'facility',
    ]
admin.site.register(FacilityType,FacilitytypeAdmin)


class FacilitiesAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'university',
        'facility',
        'name',
        'image',
        'distance',
        'fee',
        
    ]
admin.site.register(Facilities,FacilitiesAdmin)

class FactAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'university',
        'facts',
    ]
admin.site.register(Facts,FactAdmin)


class UniversityimageAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'university',
        'image',
    ]
admin.site.register(UniversityImages,UniversityimageAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'university',
        'course_type',
        'course_name',
        'icon',
        'duration',
        'duration_description',
        'course_image',
        'course_details',
        'video',
        'audio',
        'eligibility',
        'eligibility_description',
        'admission_procedure',
        'semester_fee',
        'year_fee',
        'full_fee',
        'fees_description',
        'syllabus',
        'slug',
    ]
admin.site.register(Course,CourseAdmin)

class CourseSpecializationAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'course',
        'specialization',
    ]
admin.site.register(CourseSpecialization,CourseSpecializationAdmin)

# class SpecializationAdmin(admin.ModelAdmin):
#     list_display=[
#         'id',
#         'specialization_name',
#     ]
# admin.site.register(Specialization,SpecializationAdmin)

class CountryAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'country',
        'flag',
    ]
admin.site.register(Country,CountryAdmin)

class FaqAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'course',
        'specialization',
        'faq_question',
        'faq_answer',
    ]
admin.site.register(Faq,FaqAdmin)




class UniversityBannerAdmin(admin.ModelAdmin):
    list_display=[
        'banner',
        'banner_url',
       ]
admin.site.register(UniversityBanner,UniversityBannerAdmin)

class PlacementPartnersAdmin(admin.ModelAdmin):
    list_display=[
        'university',
        'placement_partner_name',
        'placement_partner_logo',
    ]
admin.site.register(PlacementPartners,PlacementPartnersAdmin)



class CurrencySymbolAdmin(admin.ModelAdmin):
    list_display=[
        'symbol',
        'symbol_name',
        'source_currency',
        'order_id',
    ]
admin.site.register(CurrencySymbol,CurrencySymbolAdmin)

class AccreditationAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'approved_by',
        'name',
        'logo',
    ]
admin.site.register(Accreditation,AccreditationAdmin)

class AccreditationPointAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'approval',
        'points'
    ]
admin.site.register(AccreditationPoints,AccreditationPointAdmin)

class AdmissionProcedureAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'course',
        'specialization',
        'points',
    ]
admin.site.register(AdmissionProcedures,AdmissionProcedureAdmin)

class SpecializationAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'university',
        'course',
        'specialization_name',
        'duration',
        'duration_description',
        'specialization_image',
        'specialization_details',
        'video',
        'audio',
        'eligibility',
        'eligibility_description',
        'admission_procedure',
        'semester_fee',
        'year_fee',
        'full_fee',
        'fees_description',
        'syllabus',
        'slug',
    ]
admin.site.register(Specialization,SpecializationAdmin)


class UniversityDocumentsAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'student',
        'university',
        'document_name',
        'document'
    ]
admin.site.register(UniversityDocuments,UniversityDocumentsAdmin)


class StatesAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'country',
        'state_name',
    ]
admin.site.register(States,StatesAdmin)

class AlumniTalkAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'name',
        'review',
        'rating',
    ]
admin.site.register(AlumniTalk,AlumniTalkAdmin)

# Register your models here.
