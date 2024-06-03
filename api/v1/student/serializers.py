from rest_framework import serializers
from api.v1.question.serializers import OptionSerializer
from student.models import StudentProfile,ReviewStudent,RecordAnswer,StudentWishList,StudentRecord,Enquiry,CollageSuggestion
from question.models import Options
from course.models import Country,University,UniversityDocuments
import os

class CreateStudentRecordSerializer(serializers.Serializer):
    student = serializers.CharField()
    course = serializers.CharField()
    university=serializers.CharField()

class StudentDocumentSerializer(serializers.ModelSerializer):
    grade_10_name=serializers.SerializerMethodField()
    grade_12_name=serializers.SerializerMethodField()
    degree_name=serializers.SerializerMethodField()
    passport_name=serializers.SerializerMethodField()
    visa_name=serializers.SerializerMethodField()
    personal_id_name=serializers.SerializerMethodField()
    class Meta:
        model=StudentRecord
        fields=(
            'id',
            'student',
            'grade_10_certificate',
            'grade_10_name',
            'grade_12_certificate',
            'grade_12_name',
            'degree_certificate',
            'degree_name',
            'passport',
            'passport_name',
            'visa',
            'visa_name',
            'personal_id',
            'personal_id_name',
        )
    def get_grade_10_name(self,instance):
        if instance:
            file_path= instance.grade_10_certificate.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None
    def get_grade_12_name(self,instance):
        if instance:
            file_path= instance.grade_12_certificate.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None
    def get_degree_name(self,instance):
        if instance:
            file_path=instance.degree_certificate.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None
    def get_visa_name(self,instance):
        if instance:
            file_path=instance.visa.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None
    def get_passport_name(self,instance):
        if instance:
            file_path=instance.passport.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None
    def get_personal_id_name(self,instance):
        if instance:
            file_path= instance.personal_id.name
            file_name = os.path.basename(file_path)
            return file_name
        else:
            return None

class StudentRecordSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    university_logo=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    country=serializers.SerializerMethodField()
    documents=serializers.SerializerMethodField()
    class Meta:
        model=StudentRecord
        fields=(
            'id',
            'student',
            'university',
            'university_name',
            'university_logo',
            'course',
            'status',
            'course_name',
            'country',
            'documents',
            'application_date',
        )
    def get_university_name(self,instance):
        if instance.university.university_name:
            return instance.university.university_name
        else:
            return None
    def get_university_logo(self,instance):
        if instance.university.university_logo:
            request = self.context['request']
            return request.build_absolute_uri(instance.university.university_logo.url)
        else:
            return None
    def get_course_name(self,instance):
        if instance.course.course_name:
            return instance.course.course_name
        else:
            return None
    def get_country(self,instance):
        if instance.university.country:
            countries = instance.university.country.all()
            country_list = [country.country for country in countries]
            return country_list
          
        else:
            return None
    def get_documents(self,instance):
        if instance.university:
            u=instance.university.id
            request = self.context["request"]

            if (doc:=UniversityDocuments.objects.filter(student=instance,university=u,is_deleted=False)).exists():
                serialized_data=ListUniversityDocumentSerializer(doc,
                                                     context={
                                                         "request":request,
                                                     },many=True,).data
      
                return serialized_data
            else:
                None
        else:
            return None

class ListUniversityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=UniversityDocuments
        fields=(
            'id',
            'student',
            'university',
            'document_name',
            'document',
        )
   


class StudentSingleRecordViewSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    country=serializers.SerializerMethodField()
    recordanswer=serializers.SerializerMethodField()
    class Meta:
        model=StudentRecord
        fields=(
            'student',
            'course',
            'course_name',
            'university',
            'university_name',
            'status',
            'grade_10_certificate',
            'grade_12_certificate',
            'degree_certificate',
            'passport',
            'visa',
            'personal_id',
            'country',
            'recordanswer',
            'application_date',
        )
    def get_university_name(self,instance):
        if instance.university.university_name:
            return instance.university.university_name
        else:
            return None
    def get_course_name(self,instance):
        if instance.course.course_name:
            return instance.course.course_name
        else:
            return None
    def get_country(self,instance):
        if instance.university.country:
            countries = instance.university.country.all()
            country_list = [country.country for country in countries]
            return country_list
          
        else:
            return None
    def get_recordanswer(self,instance):
        if instance.student:
            request = self.context["request"]
            s_id=instance.student.id
            record=RecordAnswer.objects.filter(userid=s_id,is_deleted=False)
            serialized_data=RecordAnswerviewSerializer(record,
                                                   context={
                                                       "request":request,
                                                   },many=True).data
            return serialized_data
        else:
            return None
            

class StudentRecordViewSerializer(serializers.ModelSerializer):
    student_name=serializers.SerializerMethodField()
    student_email=serializers.SerializerMethodField()
    student_mobile=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    country=serializers.SerializerMethodField()
    university=serializers.SerializerMethodField()
    service=serializers.SerializerMethodField()
    course_type=serializers.SerializerMethodField()
    class Meta:
        model=StudentRecord
        fields=(
            'id',
            'student',
            'student_name',
            'student_email',
            'student_mobile',
            'course',
            'course_name',
            'country',
            'grade_10_certificate',
            'grade_12_certificate',
            'degree_certificate',
            'passport',
            'visa',
            'personal_id',
            'university',
            'status',
            'application_date',
            'service',
            'course_type',
        )
    def get_student_name(self,instance):
        if instance.student.name:
            return instance.student.name
        else:
            return None
    def get_student_email(self,instance):
        if instance.student.email:
            return instance.student.email
        else:
            return None
    def get_student_mobile(self,instance):
        if instance.student.mobile:
            return instance.student.mobile
        else:
            return None
    def get_course_name(self,instance):
        if instance.course.course_name:
            return instance.course.course_name
        else:
            return None
    def get_country(self,instance):
        if instance.university.country:
            countries = instance.university.country.all()
            country_list = [country.country for country in countries]
            return country_list
          
        else:
            return None
    def get_university(self,instance):
        if instance.university.university_name:
            return instance.university.university_name
        else:
            return None
    def get_service(self,instance):
        if instance.university:
            return instance.university.service.service
        else:
            return None
    def get_course_type(self,instance):
        if instance.course:
            return instance.course.course_type.course_type
        else:
            return None
            


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentProfile
        fields=(
            'name',
            'email',
            'country_code',
            'mobile',
            'gender',
            'dob',
            'status',
            'register_date',
        )

class AddStudentProfileSerializer(serializers.Serializer):
    name=serializers.CharField()
    # email=serializers.CharField()
    mobile=serializers.IntegerField()
    # gender=serializers.CharField()
    # dob=serializers.DateField()
    
class LoginSerializer(serializers.Serializer):
    mobile = serializers.IntegerField()

class ReviewStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewStudent
        fields=(
            'university',
            'name',
            'rating',
            'review',
    )


class RecordAnswerSerializer(serializers.ModelSerializer):
    question=serializers.SerializerMethodField()
    option_name=serializers.SerializerMethodField()
    options=serializers.SerializerMethodField()
    class Meta:
        model=RecordAnswer
        fields=(
            'id',
            'userid',
            'question',
            'option',
            'option_name',
            'options',
        )
    def get_question(self,instance):
        if instance.option.question:
            return instance.option.question.question
        else:
            return None
    def get_option_name(self,instance):
        if instance:
            return instance.option.options
        else:
            return None
    def get_options(self,instance):
        if instance.option.question:
            request = self.context["request"]
            options = Options.objects.filter(question=instance.option.question)
            serialized_data=OptionSerializer(options,
                                             context={
                                                 "request":request,
                                             },many=True).data
            
            return serialized_data
        else:
             return None
    # def get_userid(self,instance):
    #     if instance.userid:
    #         return instance.userid.name
    #     else:
    #         return None
   


class RecordAnswerviewSerializer(serializers.ModelSerializer):
    question=serializers.SerializerMethodField()
    option_name=serializers.SerializerMethodField()
    class Meta:
        model=RecordAnswer
        fields=(
            'id',
            'userid',
            'question',
            'option',
            'option_name',
        )
    def get_question(self,instance):
        if instance.option.question:
            return instance.option.question.question
        else:
            return None
    def get_option_name(self,instance):
        if instance:
            return instance.option.options
        else:
            return None

class AddWishListSerializer(serializers.Serializer):
    student = serializers.CharField()
    university = serializers.CharField()


class StudentWishListSerializer(serializers.ModelSerializer):
    university_name=serializers.SerializerMethodField()
    university_image=serializers.SerializerMethodField()
    course_name=serializers.SerializerMethodField()
    country=serializers.SerializerMethodField()

    class Meta:
        model = StudentWishList
        fields = (
            'id',
            'university',
            'university_name',
            'university_image',
            'course',
            'course_name',
            'country',
        )

    def get_university_name(self, instance):
        if instance.university:
            return instance.university.university_name
        else:
            return None
            
    def get_university_image(self, instance):
        request = self.context['request']
        if instance.university.university_logo:
            return request.build_absolute_uri(instance.university.university_logo.url)
        else:
            return None
    def get_course_name(self, instance):
        if instance.course:
            return instance.course.course_name
        else:
            return None
    def get_country(self,instance):
        if instance.university.country:
            countries = instance.university.country.all()
            country_list = [country.country for country in countries]
            return country_list      
        else:
            return None





class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model=Enquiry
        fields=(
            'id',
            'name',
            'last_name',
            'email',
            'phone',
            'message',
            'is_read',
            'enquiry_date',
        )

class AddEnquirySerializer(serializers.Serializer):
    name=serializers.CharField()
    phone=serializers.IntegerField()

class SuggestionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollageSuggestion
        fields = ('service','university','profile_image','full_name','email','mobile')