from rest_framework import serializers
from course.models import University,Facts,Course,UniversityImages,States,AlumniTalk,FacilityType,Accreditation,UniversityDocuments,Specialization,AccreditationPoints,CurrencySymbol,Facilities,Country,AdmissionProcedures,CourseSpecialization,Faq,UniversityBanner,PlacementPartners
from service.models import CourseType
from api.v1.student.serializers import StudentRecordSerializer
from api.v1.service.serializers import CourseTypeSerializer,ServiceSerializer
from api.v1.question.serializers import *
from django.db.models import Max, Min,IntegerField
from django.db.models.functions import Cast
from django.conf import settings
from question.models import *
from service.models import *


class AddUniversitySerializer(serializers.Serializer):
    university_logo=serializers.FileField()
    university_name=serializers.CharField()
    about_university=serializers.CharField()
    slug=serializers.CharField()
    
class UniversitylistSerializer(serializers.ModelSerializer):
    facts=serializers.SerializerMethodField()
    approval=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    facility=serializers.SerializerMethodField()
    wishlist=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
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
            'country',
            'credit_points',
            'e_learning_facility',
            'placement_assistance',
            'industry_ready',
            'satisfied_student',
            'pros',
            'world_ranking',
            'country_ranking',
            'nirf_training',
            'wes_approval',
            'facts',
            'approval',
            'course',
            'facility', 
            'rating',
            'wishlist',
            'top_rated',
            'slug',
        )
    def get_course(self,instance):
        request = self.context["request"]
        course = self.context["course_name"]
        serialized_data = []

        if instance:
            university = instance.id
            course_data = Course.objects.filter(university=university, course_name=course)

            if course_data.exists():
                serialized_data = CourseSerializer(
                    course_data,
                    context={
                        "request": request
                    },
                    many=True
                ).data

        return serialized_data

    
    def get_facts(self,instance):
        if instance:
            fact=list(instance.facts_set.filter(is_deleted=False).values('id','facts'))
            return fact
        else:
            return None
    
    def get_approval(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.approved_by.all()

            serialized_data = AccreditationSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    def get_facility(self,instance):
        if instance:
            facilities=list(instance.facilities_set.filter(is_deleted=False).values('facility','facility__facility').distinct('facility'))
            return facilities
        else:
            return None
    def get_wishlist(self,instance):
        request = self.context["request"]
        userid = self.context["userid"]
        if instance:
            wishlist = instance.studentwishlist_set.filter(student=userid,university=instance, is_deleted=False).values_list('is_active', flat=True).first()            
            return wishlist
        else:
            return None


class UniversitylistSpecializationSerializer(serializers.ModelSerializer):
    facts=serializers.SerializerMethodField()
    approval=serializers.SerializerMethodField()
    # course=serializers.SerializerMethodField()
    specialization=serializers.SerializerMethodField()
    facility=serializers.SerializerMethodField()
    wishlist=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
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
            'country',
            'credit_points',
            'world_ranking',
            'e_learning_facility',
            'country_ranking',
            'placement_assistance',
            'industry_ready',
            'satisfied_student',
            'pros',
            'nirf_training',
            'wes_approval',
            'facts',
            'approval',
            # 'course',
            'specialization',
            'facility', 
            'rating',
            'wishlist',
            'top_rated',
            'slug',
        )

    def get_specialization(self,instance):
        request = self.context["request"]
        course = self.context["course_name"]

        specialization=self.context['specialization']
        serialized_data = []

        if instance:
            university = instance.id
            s_data=Specialization.objects.filter(university=university,course__course_name=course,specialization_name=specialization)
            if s_data.exists():
                serialized_data = SpecializationSerializer(
                    s_data,
                    context={
                        "request": request
                    },
                    many=True
                ).data
                return serialized_data   
            else:
                return None
        else:
            return None
    
    def get_facts(self,instance):
        if instance:
            fact=list(instance.facts_set.filter(is_deleted=False).values('id','facts'))
            return fact
        else:
            return None
    
    def get_approval(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.approved_by.all()

            serialized_data = AccreditationSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    def get_facility(self,instance):
        if instance:
            facilities=list(instance.facilities_set.filter(is_deleted=False).values('facility','facility__facility').distinct('facility'))
            return facilities
        else:
            return None
    def get_wishlist(self,instance):
        request = self.context["request"]
        userid = self.context["userid"]
        if instance:
            wishlist = instance.studentwishlist_set.filter(student=userid,university=instance, is_deleted=False).values_list('is_active', flat=True).first()            
            return wishlist
        else:
            return None


class AddAccreditationSerializer(serializers.Serializer):
    approved_by=serializers.CharField()
    name=serializers.CharField()
    logo=serializers.FileField()

class AddAccreditationPointsSerializer(serializers.Serializer):
    points=serializers.CharField()

class AccreditationPointSerializer(serializers.ModelSerializer):
    class Meta:
        model=AccreditationPoints
        fields=(
            'id',
            'approval',
            'points',
        )

class AccreditationSerializer(serializers.ModelSerializer):
    points=serializers.SerializerMethodField()
    class Meta:
        model=Accreditation
        fields=(
            'id',
            'approved_by',
            'name',
            'logo',
            'points',
        )
    def get_points(self,instance):
        if instance:
            accreditation_points=list(instance.accreditationpoints_set.filter(is_deleted=False).values('approval','points'))
            return accreditation_points
        else:
            return None





class UniversitySerializer(serializers.ModelSerializer):
    facts=serializers.SerializerMethodField()
    approval=serializers.SerializerMethodField()
    facility=serializers.SerializerMethodField()
    service_name=serializers.SerializerMethodField()
    country=serializers.SerializerMethodField()
    state=serializers.SerializerMethodField()
    options=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
            'id',
            'service',
            'service_name',
            'university_logo',
            'university_image',
            'university_name',
            'about_university',
            'sample_certificate',
            'prospectus',
            'student_choice',
            'student_review',
            'country',
            'state',
            'options',
            'facts',
            'approval',
            'facility',
            'credit_points',
            'e_learning_facility',
            'placement_assistance',
            'industry_ready',
            'satisfied_student',
            'pros',
            'world_ranking',
            'country_ranking',
            'nirf_training',
            'wes_approval',
            'rating',
            'slug',
        )
   
    def get_service_name(self,instance):
        if instance:
            return instance.service.service
        else:
            return None
        
    def get_facts(self,instance):
        if instance:
            fact=list(instance.facts_set.filter(is_deleted=False).values('id','facts'))
            return fact
        else:
            return None
    def get_approval(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.approved_by.all()

            serialized_data = AccreditationSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    def get_country(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.country.all()

            serialized_data = CountrySerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    def get_state(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.state.all()

            serialized_data = StateSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    def get_options(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.options.all()

            serialized_data = OptionSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    
    def get_facility(self,instance):
        if instance:
            facilities=list(instance.facilities_set.filter(is_deleted=False).values('facility','facility__facility').distinct('facility'))
            return facilities
        else:
            return None

class PopularUniversitySerializer(serializers.ModelSerializer):
    service=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
            'id',
            'university_name',
            'service',
        )
    def get_service(self,instance):
        if instance:
            s={"service":instance.service.service}
            return s
        else:
            return None
   
class AddFacilityTypeSerializer(serializers.Serializer):
    facility=serializers.CharField()

class FacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacilityType
        fields=(
            'id',
            'facility',
        )
class AddFacilitiesSerializer(serializers.Serializer):
    name=serializers.CharField()
    distance=serializers.CharField()
    fee=serializers.CharField()

class FacilitiesSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    facility_name=serializers.SerializerMethodField()
    class Meta:
        model=Facilities
        fields=(
            'id',
            'university',
            'facility',
            'university_name',
            'facility_name',
            'name',
            'image',
            'distance',
            'fee',
        )
    def get_university_name(self,instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None
    def get_facility_name(self,instance):
        if instance.facility:
            return instance.facility.facility
        else:
            return None


class AddFactSerializer(serializers.Serializer):
    facts=serializers.CharField()

class FactSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    class Meta:
        model=Facts
        fields=(
            'university',
            'university_name',
            'id',
            'facts',
           
        )
    def get_university_name(self,instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None



class AddUniversityImageSerializer(serializers.Serializer):
    image=serializers.FileField()

class UniversityImageSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    class Meta:
        model=UniversityImages
        fields=(
            'university',
            'university_name',
            'id',
            'image',
           
        )
    def get_university_name(self,instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None

class CourseviewSerializer(serializers.ModelSerializer):
    service=serializers.SerializerMethodField()
    service_type=serializers.SerializerMethodField()
    university_count=serializers.SerializerMethodField()
    specialization=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=(
            'id',
            'course_name',
            'icon',
            'duration',
            'service',
            'service_type',
            'course_type',
            'university', 
            'university_count',
            'specialization',
        )
    def get_service(self, instance):
        coursetype = instance.course_type
        if coursetype and coursetype.service:
            return coursetype.service.id 
        else:

            return None  
    def get_service_type(self, instance):
        coursetype = instance.course_type
        if coursetype and coursetype.service:
            return coursetype.service.service
        else:

            return None  
    def get_university_count(self,instance):
        course_name=instance.course_name
        service=instance.course_type.service.id
        if course_name:
            count = Course.objects.filter(course_name=course_name, course_type__service=service).values('university').distinct().count()
            return count
        else:
            return None
    def get_specialization(self,instance):
        course=instance.id
        request = self.context["request"]
        specialization=Specialization.objects.filter(course=course,is_deleted=False)
        if specialization:
            s=SpecializationSerializer(specialization,context={'request':request},many=True,).data
            return s
        else:
            return None


# class SpecializationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Specialization
#         fields=(
#             'id',
#             'specialization_name'
#         )

# class CourseSpecialSerializer(serializers.ModelSerializer):
#     specialization = serializers.SerializerMethodField()
#     class Meta:
#         model=Course
#         fields=(
#             'specialization', 
#         )
#     def get_specialization(self,instance):
#         request = self.context["request"]
#         if instance:
#             selected_categories = instance.specialization.all()
#             serialized_data = SpecializationSerializer(
#                 selected_categories,
#                 context = {
#                     "request" : request
#                 },
#                 many=True
#             ).data
      
#             return serialized_data
#         else:
#             return None
        
    

class CourseCountrySerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=(
            
            'university',
            
        )

    def get_university(self,instance):
        request = self.context["request"]
        if instance.university:
            selected_categories = instance.university.country.all()
            serialized_data = CountrySerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None


class CourseStateSerializer(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=(
            
            'university',
            
        )

    def get_university(self,instance):
        request = self.context["request"]
        if instance.university:
            selected_categories = instance.university.state.all()
            serialized_data = StateSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None


class AddCourseSerializer(serializers.Serializer):
    course_name=serializers.CharField()
    icon=serializers.ImageField(required=False)
    duration=serializers.CharField()
    course_image=serializers.FileField()
    eligibility=serializers.CharField()
    syllabus=serializers.FileField(required=False)
    slug=serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    admission_procedure_points=serializers.SerializerMethodField()
    course_type=serializers.SerializerMethodField()
    specialization=serializers.SerializerMethodField()
    service=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=(
            'id',
            'course_name',
            'course_type',
            'service',
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
            'admission_procedure_points',
            'semester_fee',
            'converted_sem_fee',
            'year_fee',
            'converted_year_fee',
            'full_fee',
            'converted_full_fee',
            'fees_description',
            'syllabus',
            'university',
            'slug',
            'specialization',
            
        )
    def get_course_type(self,instance):
        if instance:
            return instance.course_type.course_type
        else:
            return None
    def get_service(self,instance):
        if instance:
            return instance.course_type.service.id
        else:
            return None
    def get_admission_procedure_points(self,instance):
        if instance:
            points=list(instance.admissionprocedures_set.filter(course=instance,is_deleted=False).values('id','points'))
            return points
        else:
            return None
    def get_specialization(self,instance):
        if instance:
            request = self.context["request"]
            course_name=instance.course_name
            s=Specialization.objects.filter(course__course_name=course_name,is_deleted=False).distinct('specialization_name')
            if s:
                serialized_data=SpecializationSerializer(s,
                                                        context={"request":request,
                                                        },
                                                        many=True).data
                return serialized_data
            else:
                return None
        else:
            return None




class AddCourseSpecializationSerializer(serializers.Serializer):
    specialization=serializers.CharField()


class CourseSpecializationSerializer(serializers.ModelSerializer):
    course=serializers.SerializerMethodField()
    course_duration=serializers.SerializerMethodField()
    course_id=serializers.SerializerMethodField()
    course_type=serializers.SerializerMethodField()
    service=serializers.SerializerMethodField()
    class Meta:
        model=CourseSpecialization
        fields=(
            'id',
            'course',
            'course_id',
            'course_type',
            'course_duration',
            'service',
            'specialization',
            
        )
    def get_course(self,instance):
        if instance.course:
            return instance.course.course_name
        else:
            return None
    def get_course_id(self,instance):
        if instance.course:
            return instance.course.id
        else:
            return None
    def get_course_type(self,instance):
        if instance.course:
            return instance.course.course_type.id
        else:
            return None
    def get_course_duration(self,instance):
        if instance.course:
            return instance.course.duration
        else:
            return None
    def get_service(self,instance):
        if instance.course:
            return instance.course.course_type.service.id
        else:
            return None

class AddCountrySerializer(serializers.Serializer):
    country=serializers.CharField()
    flag=serializers.FileField()

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields=(
            'id',
            'country',
            'flag',
        )

class AddFaqSerializer(serializers.Serializer):
    faq_question=serializers.CharField()
    faq_answer=serializers.CharField()

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model=Faq
        fields=(
            'id',
            'faq_question',
            'faq_answer',
        )


class UniversityBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=UniversityBanner
        fields=(
            'id',
            'banner',
            'banner_url',
        )

class AddUniversityBannerSerializer(serializers.Serializer):
    banner=serializers.FileField()


class PlacementPartnerSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    class Meta:
        model=PlacementPartners
        fields=(
            'id',
            'university',
            'university_name',
            'placement_partner_name',
            'placement_partner_logo',
        )
    def get_university_name(self,instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None

class AddplacementpartnerSerializer(serializers.Serializer):
    placement_partner_name=serializers.CharField()
    placement_partner_logo=serializers.FileField()


class AddadmissionProcedureSerializer(serializers.Serializer):
    points=serializers.CharField()

class AdmissionProcedureSerializer(serializers.ModelSerializer):
    course_name=serializers.SerializerMethodField()
    specialization_name=serializers.SerializerMethodField()
    class Meta:
        model=AdmissionProcedures
        fields=(
            'id',
            'course',
            'course_name',
            'specialization',
            'specialization_name',
            'points',
        )
    def get_course_name(self,instance):
        if instance and instance.course:
            return instance.course.course_name
        else:
            return None
    def get_specialization_name(self, instance):
        if instance and instance.specialization:  
            return instance.specialization.specialization_name
        else:
            return None


class ListCourseSpecializationUniversity(serializers.ModelSerializer):
    university = serializers.SerializerMethodField()
    # min_fee=serializers.SerializerMethodField()
    # max_fee=serializers.SerializerMethodField()
    class Meta:
        model=Specialization
        fields=(
            'id',
            'specialization_name',
            'course',
            'university',
            # 'min_fee',
            # 'max_fee',
        
        )
    def get_university(self, instance):
        request = self.context["request"]
        serialized_data = []
        fee_range=request.GET.get('fee_range')
        # course_name=instance.course.course_name
        if fee_range and instance.specialization_name and instance.course:
            queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course__course_name=instance.course.course_name)
            min_year_fee = queryset.aggregate(min_value=Min('year_fee'))['min_value']
            universities=Specialization.objects.filter(year_fee__range=(min_year_fee, fee_range),course__course_name=instance.course.course_name,specialization_name=instance.specialization_name)
            serialized_data = UniversitySpecializationSerializer(
                            universities,
                            context={
                                "request": request
                            },
                            many=True
                        ).data
        elif instance.specialization_name and instance.course:
            universities = Specialization.objects.filter(specialization_name=instance.specialization_name,course__course_name=instance.course.course_name)

            serialized_data = UniversitySpecializationSerializer(
                universities,
                context={
                    "request": request
                },
                many=True
            ).data
        else:
            return None
     
        return serialized_data
    # def get_min_fee(self,instance):
    #     if instance.course and instance.specialization_name:
    #         queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course=instance.course)
    #         min_full_fee = queryset.aggregate(min_full_fee=Min('full_fee'))['min_full_fee']
    #         return min_full_fee
    #     else:
    #         return None
    # def get_max_fee(self,instance):
    #     if instance.course and instance.specialization_name:
    #         queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course=instance.course)
        
    #         max_full_fee = queryset.aggregate(max_full_fee=Max('full_fee'))['max_full_fee']        
          
    #         return max_full_fee
    #     else:
    #         return None

class AddcurrencySerializer(serializers.Serializer):
    symbol=serializers.CharField()
    symbol_name=serializers.CharField()

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model=CurrencySymbol
        fields=(
            'id',
            'symbol',
            'symbol_name',
        )

class SpecializationSerializer(serializers.ModelSerializer):
    course_name=serializers.SerializerMethodField()
    university_name = serializers.SerializerMethodField()
    course_type=serializers.SerializerMethodField()
    service=serializers.SerializerMethodField()
    count=serializers.SerializerMethodField()
    admission_procedure_points=serializers.SerializerMethodField()
    class Meta:
        model=Specialization
        fields=(
            'id',
            'slug',
            'university',
            'university_name',
            'course',
            'course_name',
            'course_type',
            'service',
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
            'admission_procedure_points',
            'semester_fee',
            'converted_sem_fee',
            'year_fee',
            'converted_year_fee',
            'full_fee',
            'converted_full_fee',
            'fees_description',
            'syllabus',
            'count',
          
            
        )
    def get_course_name(self,instance):
        if instance.course:
            return instance.course.course_name
        else:
            return None
    def get_university_name(self,instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None
    def get_course_type(self,instance):
        if instance.course:
            return instance.course.course_type.id
        else:
            return None
    def get_service(self,instance):
        if instance.course:
            return instance.course.course_type.service.id
        else:
            return None
    def get_count(self,instance):
        if instance:
            university_count=Specialization.objects.filter(specialization_name=instance.specialization_name,course__course_name=instance.course.course_name,is_deleted=False).values('university').distinct().count()
            return university_count
        else:
            return None
    def get_admission_procedure_points(self,instance):
        if instance:
            points=list(instance.admissionprocedures_set.filter(specialization=instance,is_deleted=False).values('id','points'))
            return points
        else:
            return None
    
class AddSpecializationSerializer(serializers.Serializer):
    specialization_name=serializers.CharField()
    slug=serializers.CharField()
    # year_fee=serializers.CharField()


class AddUniversityDocumentSerializer(serializers.Serializer):
    document_name=serializers.CharField()
    document=serializers.FileField()

class UniversityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=UniversityDocuments
        fields=(
            'id',
            'student',
            'university',
            'document_name',
            'document',
        )

class StateSerializer(serializers.ModelSerializer):
    country_name=serializers.SerializerMethodField()
    class Meta:
        model=States
        fields=(
            'id',
            'country',
            'country_name',
            'state_name',            
        )
    def get_country_name(self,instance):
        if instance.country.country:
            return instance.country.country
        else:
            return None

class UniversitySpecializationSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    university_logo=serializers.SerializerMethodField()
    university_image=serializers.SerializerMethodField()
    university_images=serializers.SerializerMethodField()
    rating=serializers.SerializerMethodField()
    approvals=serializers.SerializerMethodField()
    class Meta:
        model=Specialization
        fields=(
            'university',
            'university_name',
            'university_logo',
            'university_image',
            'university_images',
            'year_fee',
            'full_fee',
            'rating',
            'approvals',
        
        )
    def get_university_name(self,instance):
        if instance.university.university_name:
            return instance.university.university_name
        else:
            return None
    def get_university_logo(self,instance):
        if instance.university.university_logo:
            request = self.context.get('request')
            logo=instance.university.university_logo.url
            return request.build_absolute_uri(logo)
        else:
            return None
    def get_university_image(self,instance):
        if instance.university.university_image:
            request = self.context.get('request')
            image=instance.university.university_image.url
            return request.build_absolute_uri(image)
        else:
            return None
    
    def get_university_images(self,instance):
        request = self.context["request"]
        if instance.university:
            u=instance.university
            selected_images = UniversityImages.objects.filter(university=u,is_deleted=False)

            serialized_data = UniversityImageSerializer(
                selected_images,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    


    def get_rating(self,instance):
        if instance.university.rating:
            return instance.university.rating
        else:
            return None
    def get_approvals(self,instance):
            request = self.context["request"]
            if instance.university:
                selected_categories = instance.university.approved_by.all()

                serialized_data = AccreditationSerializer(
                    selected_categories,
                    context = {
                        "request" : request
                    },
                    many=True
                ).data

                return serialized_data
            else:
                return None
    




class CompareUniversitySerializer(serializers.ModelSerializer):
    facts=serializers.SerializerMethodField()
    approval=serializers.SerializerMethodField()
    facility=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    placement=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
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
            'country',
            'facts',
            'approval',
            'facility',
            'credit_points',
            'e_learning_facility',
            'placement_assistance',
            'industry_ready',
            'satisfied_student',
            'pros',
            'world_ranking',
            'country_ranking',
            'nirf_training',
            'wes_approval',
            'rating',
            'placement',
            'course',
        )    
    def get_facts(self,instance):
        if instance:
            fact=list(instance.facts_set.filter(is_deleted=False).values('id','facts'))
            return fact
        else:
            return None
    def get_approval(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.approved_by.all()

            serialized_data = AccreditationSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    def get_facility(self,instance):
        if instance:
            facilities=list(instance.facilities_set.filter(is_deleted=False).values('facility','facility__facility').distinct('facility'))
            return facilities
        else:
            return None
    def get_placement(self,instance):
        if instance:
            placement=list(instance.placementpartners_set.filter(is_deleted=False).values('id','placement_partner_name','placement_partner_logo'))
            request = self.context.get('request') 
            for image in placement:
                if image['placement_partner_logo']  is not None:
                    image['placement_partner_logo'] = request.build_absolute_uri(settings.MEDIA_URL + image['placement_partner_logo'])
                else:
                    image['placement_partner_logo'] =None

            return placement
        else:
            return None
    def get_course(self,instance):
        request = self.context["request"]
        course = self.context["course"]
        serialized_data = []

        if instance:
            university = instance.id
            course_data = Course.objects.filter(university=university, course_name=course)

            if course_data.exists():
                serialized_data = CourseSerializer(
                    course_data,
                    context={
                        "request": request
                    },
                    many=True
                ).data

        return serialized_data




class SingleUniversityDetailsSerializer(serializers.ModelSerializer):
    facts=serializers.SerializerMethodField()
    approval=serializers.SerializerMethodField()
    facility=serializers.SerializerMethodField()
    course=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
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
            'country',
            'facts',
            'approval',
            'facility',
            'credit_points',
            'e_learning_facility',
            'placement_assistance',
            'industry_ready',
            'satisfied_student',
            'pros',
            'world_ranking',
            'country_ranking',
            'nirf_training',
            'wes_approval',
            'rating',
            'course',
        )
   
    
    def get_facts(self,instance):
        if instance:
            fact=list(instance.facts_set.filter(is_deleted=False).values('id','facts'))
            return fact
        else:
            return None
    def get_approval(self,instance):
        request = self.context["request"]
        if instance:
            selected_categories = instance.approved_by.all()

            serialized_data = AccreditationSerializer(
                selected_categories,
                context = {
                    "request" : request
                },
                many=True
            ).data

            return serialized_data
        else:
            return None
    
    def get_facility(self,instance):
        if instance:
            facilities=list(instance.facilities_set.filter(is_deleted=False).values('facility','facility__facility').distinct('facility'))
            return facilities
        else:
            return None
    def get_course(self,instance):
        request = self.context["request"]
        course = self.context["course"]
        serialized_data = []

        if instance:
            university = instance.id
            course_data = Course.objects.filter(university=instance, id=course)

            if course_data.exists():
                serialized_data = CourseSerializer(
                    course_data,
                    context={
                        "request": request
                    },
                    many=True
                ).data

        return serialized_data

        
        

class SuggestCourseSerializer(serializers.ModelSerializer):
    admission_procedure_points=serializers.SerializerMethodField()
    course_type=serializers.SerializerMethodField()
    specialization=serializers.SerializerMethodField()
    class Meta:
        model=Course
        fields=(
            'id',
            'course_name',
            'course_type',
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
            'admission_procedure_points',
            'semester_fee',
            'converted_sem_fee',
            'year_fee',
            'converted_year_fee',
            'full_fee',
            'converted_full_fee',
            'fees_description',
            'syllabus',
            'university',
            'slug',
            'specialization',
            
        )
    def get_course_type(self,instance):
        if instance:
            return instance.course_type.course_type
        else:
            return None
    def get_admission_procedure_points(self,instance):
        if instance:
            points=list(instance.admissionprocedures_set.filter(is_deleted=False).values('id','points'))
            return points
        else:
            return None
    
    def get_specialization(self,instance):
        if instance:
            if (s:=Specialization.objects.filter(course=instance,is_deleted=False)).exists():
                request = self.context["request"]
                serialized_data=SpecializationSerializer(s,
                                                         context={
                                                             "request":request,
                                                         },many=True).data
                return serialized_data
            else:
                return None



class SearchUniversitySerializer(serializers.ModelSerializer):
    course=serializers.SerializerMethodField()
    service_type=serializers.SerializerMethodField()
    class Meta:
        model=University
        fields=(
            'id',
            'service',
            'service_type',
            'university_logo',
            'university_image',
            'university_name',
            'course',
        )
    def get_course(self,instance):
        if instance:
            request = self.context["request"]
            university = instance.university_name
            course_data = Course.objects.filter(university__university_name=university).distinct('course_name')

            if course_data.exists():
                serialized_data = CourseSerializer(
                    course_data,
                    context={
                        "request": request
                    },
                    many=True
                ).data

                return serialized_data
            else:
                return None
        else:
            return None

    def get_service_type(self,instance):
        if instance.service:
            return instance.service.service
        else:
            return None
            
   
class AlumniTalkSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    class Meta:
        model=AlumniTalk
        fields=(
            'id',
            'name',
            'review',
            'rating',
            'university',
            'university_name',
        )
    def get_university_name(self,instance):
        if instance:
            return instance.university.university_name
        else:
            return None




# class ListCourseSpecializationUniversity(serializers.ModelSerializer):
#     university = serializers.SerializerMethodField()
#     min_fee=serializers.SerializerMethodField()
#     max_fee=serializers.SerializerMethodField()
#     class Meta:
#         model=Specialization
#         fields=(
#             'id',
#             'specialization_name',
#             'year_fee',
#             'course',
#             'university',
#             'min_fee',
#             'max_fee',
        
#         )
#     def get_university(self, instance):
#         request = self.context["request"]
#         serialized_data = []
#         fee_range=request.GET.get('fee_range')
        
#         if fee_range and instance.specialization_name and instance.course:
#             queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course=instance.course)
#             min_year_fee = queryset.aggregate(min_year_fee=Min('year_fee'))['min_year_fee']
#             universities=University.objects.filter(specialization__year_fee__range=(min_year_fee, fee_range),specialization__course=instance.course,specialization__id=instance.id)
#             print(universities,"=-=-=-=-=-=-=-=-=")
#             serialized_data = UniversitySerializer(
#                             universities,
#                             context={
#                                 "request": request
#                             },
#                             many=True
#                         ).data
#         elif instance.specialization_name and instance.course:
#             universities = University.objects.filter(
#                 # course__specialization=instance.id,
#                 course=instance.course
#             )
#             serialized_data = UniversitySerializer(
#                 universities,
#                 context={
#                     "request": request
#                 },
#                 many=True
#             ).data
#         else:
#             return None
     
#         return serialized_data
#     def get_min_fee(self,instance):
#         if instance.course:
#             queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course=instance.course)
        
#             min_year_fee = queryset.aggregate(min_year_fee=Min('year_fee'))['min_year_fee']
        
          
#             return min_year_fee
#         else:
#             return None
#     def get_max_fee(self,instance):
#         if instance.course:
#             queryset = Specialization.objects.filter(specialization_name=instance.specialization_name,course=instance.course)
        
#             max_year_fee = queryset.aggregate(max_year_fee=Max('year_fee'))['max_year_fee']
        
          
#             return max_year_fee
#         else:
#             return None



# class SpecializationUniversity(serializers.ModelSerializer):
#     university = serializers.SerializerMethodField()
#     min_fee=serializers.SerializerMethodField()
#     max_fee=serializers.SerializerMethodField()
#     class Meta:
#         model=Course
#         fields=(
#             'id',
#             'university',
#             'min_fee',
#             'max_fee',
            
#         )
#     def get_university(self, instance):
#         request = self.context["request"]
#         fee_range=request.GET.get('fee_range')
#         course_name=request.GET.get('course_name')
#         if fee_range and instance:
#             queryset = Course.objects.filter(course_name=course_name)
#             min_year_fee = queryset.aggregate(min_year_fee=Min('year_fee'))['min_year_fee']
#             sp=Specialization.objects.filter(id=instance.id,course__course_name=course_name)
#             s=sp.latest('id')
#             universities=University.objects.filter(course__year_fee__range=(min_year_fee, fee_range),course__course_name=course_name,course__specialization__id=s.id)
#             serialized_data = UniversitySerializer(
#                             universities,
#                             context={
#                                 "request": request
#                             },
#                             many=True
#                         ).data
#             return serialized_data
#         elif instance:
#             universities = University.objects.filter(
                
#                 course__course_name=course_name,course__specialization__id=s
#             )
#             serialized_data = UniversitySerializer(
#                 universities,
#                 context={
#                     "request": request
#                 },
#                 many=True
#             ).data
#             return serialized_data
#         else:
#             return None
     
        
#     def get_min_fee(self,instance):
#         if instance:
#             request = self.context["request"]
#             course_name=request.GET.get('course_name')
#             queryset = Course.objects.filter(course_name=course_name)
        
#             min_year_fee = queryset.aggregate(min_year_fee=Min('year_fee'))['min_year_fee']
        
          
#             return min_year_fee
#         else:
#             return None
#     def get_max_fee(self,instance):
#         if instance:
#             request = self.context["request"]
#             course_name=request.GET.get('course_name')
#             queryset = Course.objects.filter(course_name=course_name)
        
#             max_year_fee = queryset.aggregate(max_year_fee=Max('year_fee'))['max_year_fee']
        
          
#             return max_year_fee
#         else:
#             return None
