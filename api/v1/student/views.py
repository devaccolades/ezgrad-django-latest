from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from student.models import StudentProfile,ReviewStudent,RecordAnswer,StudentRecord,StudentWishList,CustomUser,Enquiry,CollageSuggestion
from course.models import Country,University,Course,Specialization
from api.v1.course.serializers import UniversitySerializer,UniversitylistSerializer,UniversitylistSpecializationSerializer,CourseviewSerializer
from question.models import Options,Questions
from api.v1.question.serializers import OptionSerializer
from api.v1.student.serializers import RecordAnswerSerializer,AddEnquirySerializer,EnquirySerializer,CreateStudentRecordSerializer,StudentSingleRecordViewSerializer,StudentRecordViewSerializer,StudentDocumentSerializer,StudentRecordSerializer,AddWishListSerializer,StudentWishListSerializer,StudentProfileSerializer,ReviewStudentSerializer,AddStudentProfileSerializer,LoginSerializer,SuggestionAddSerializer,SuggestionSerializer,SingleCollageInfo
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from general.functions import generate_serializer_errors,check_username,randomnumber,generate_otp,send_otp_email
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
# from general.encryption import encrypt, decrypt
from rest_framework import status
import requests
import json
from general.decorators import group_required
from django.db import transaction
import traceback
from django.db.models import Q
from datetime import date,datetime
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework.views import APIView

@api_view(['GET'])
@permission_classes([AllowAny])
def general_search(request):
    try:
        q =  request.GET.get('q')
        if (course := Course.objects.filter(is_deleted=False)).exists():

            if q:
                course = course.filter(Q(course_name__icontains=q) | Q(university__university_name__icontains=q))

            serialized_data = CourseviewSerializer(
                course,
                context = {
                    "request":request,
                },
                many=True,
            ).data

            response_data={
                "StatusCode":6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "data" : {
                    "title" : "Failed",
                    "Message" : "course Not Found"
                }
            }

    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def calculate_age(request):
    today = date.today()
    birth_date =request.GET.get('birth_date')
    if birth_date:
        try:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                response_data={
                    "StatusCode":6000,
                    "data":{
                        "age":age
                    }
                }
   
        except ValueError as e:
                response_data = {
                    "StatusCode": 6001,
                    "error": str(e)
                }
    else:
        response_data = {
            "StatusCode": 6001,
            "error": "Missing or invalid birth_date parameter"
        }

    return Response({'app_data':response_data})

from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
@api_view(['POST'])
@permission_classes([AllowAny])
def register_student(request):
    response_data = {}
    try:
        serialized_data = AddStudentProfileSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data.get('name', '')
            email = request.data.get('email', '')
            country_code = request.data.get('country_code', '')
            mobile = request.data.get('mobile', '')
            gender = request.data.get('gender', '')
            dob = request.data.get('dob', '')

            with transaction.atomic():
                existing_student = StudentProfile.objects.filter(
                    Q(email=email) | Q(mobile=mobile), is_deleted=False
                ).first()

                if existing_student:
                    if name:
                        existing_student.name = name
                    if gender:
                        existing_student.gender = gender
                    if dob:
                        existing_student.dob = dob
                    if email:
                        existing_student.email = email
                    if country_code:
                        existing_student.country_code = country_code
                    existing_student.save()

                    username = existing_student.username
                    password = existing_student.password

                    headers = {"Content-Type": "application/json"}
                    data = {"username": username, "password": password}

                    protocol = "http://"
                    if request.is_secure():
                        protocol = "https://"

                    host = request.get_host()
                    url = protocol + host + "/api/token/"
                    response = requests.post(url, headers=headers, data=json.dumps(data))

                    if response.status_code == 200:
                        response = response.json()
                        response_data = {
                            "StatusCode": 6000,
                            "data": {
                                "title": "Success",
                                "message": "Updated Successfully",
                                "userid": existing_student.id,
                                "access_token": response["access"],
                                "refresh_token": response["refresh"],
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode": 6001,
                            "data": {
                                "title": "Failed",
                                "Message": "Failed to retrieve access token after update."
                            }
                        }

                else:
                    student_profile = StudentProfile.objects.create(
                        name=name, email=email, mobile=mobile, gender=gender, dob=dob, country_code=country_code
                    )
                    context = {'name': name, 'email': email, 'mobile': mobile}
                    template = get_template('index.html').render(context)
                    e = settings.EMAIL_HOST_USER
                    send_mail(
                        'Enquiry Data',
                        None, 
                        settings.EMAIL_HOST_USER,
                        [e],
                        fail_silently=False,
                        html_message=template,
                    )

                    password = User.objects.make_random_password(length=12, allowed_chars="abcdefghjkmnpqrstuvwzyx#@*%$ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
                    sliced_phone = mobile[-4:]
                    username = f'EZG{sliced_phone}{randomnumber(4)}'
                    username = check_username(username)
                    headers = {"Content-Type": "application/json"}
                    data = {"username": username, "password": password}

                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        is_active=True
                    )
                    student_profile.user = user
                    student_profile.username = username
                    student_profile.password = password
                    student_profile.save()

                    student_group, created = Group.objects.get_or_create(name='ezgrad_student')
                    student_group.user_set.add(user)

                    # protocol = "http://"
                    # if request.is_secure():
                    #     protocol = "https://"

                    # host = request.get_host()
                    # url = protocol + host + "/api/token/"
                    
                    response = get_tokens_for_user(user)
 
                    if response:
                        response_data = {
                            "StatusCode": 6000,
                            "data": {
                                "title": "Success",
                                "Message": "Registered Successfully ",
                                "userid": student_profile.id,
                                "access_token": response["access"],
                                "refresh_token": response["refresh"],
                            }
                        }
                    else:
                        response_data = {
                            "StatusCode": 6001,
                            "data": {
                                "title": "Failed",
                                "Message": "Failed to retrieve access token after registration."
                            }
                        }

        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": generate_serializer_errors(serialized_data._errors)
                }
            }

    except Exception as e:
        print(e)
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_studentprofile(request):
    q = request.GET.get('q')
    
    if (reg:=StudentProfile.objects.filter(is_deleted=False)).exists():
        enq_count=StudentProfile.objects.filter(is_deleted=False).count()
        converted=StudentProfile.objects.filter(is_deleted=False,status="converted").count()
        followup=StudentProfile.objects.filter(is_deleted=False,status="follow up").count()
        notinterested=StudentProfile.objects.filter(is_deleted=False,status="not interested").count()
        
        if q:
            std = reg.filter(
                    Q(name__icontains=q) | 
                    Q(email__icontains=q) | 
                    Q(mobile__icontains=q) |  
                    Q(country_code__icontains=q)
                )
            serialized_data=StudentProfileSerializer(std,
                                            context={
                                                "request":request,
                                            },
                                            many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "enq_count":enq_count,
                "converted":converted,
                "followup":followup,
                "notinterested":notinterested,
            }
        else:
       
            serialized_data=StudentProfileSerializer(reg,
                                            context={
                                                "request":request,
                                            },
                                            many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "enq_count":enq_count,
                "converted":converted,
                "followup":followup,
                "notinterested":notinterested,
            }   
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['PUT'])
@permission_classes([AllowAny])
def edit_studentprofile(request,pk):
    name=request.data.get('name')
    email=request.data.get('email')
    mobile=request.data.get('mobile')
    dob=request.data.get('dob')
    option=request.data.getlist('option')

    if(register:=StudentProfile.objects.filter(pk=pk)).exists():
            reg=register.latest('id')
      
            if name:
                reg.name=name
            if email:
                reg.email=email
            if mobile:
                reg.mobile=mobile
            if dob:
                reg.dob=dob
            reg.save()
           
            record_list=RecordAnswer.objects.filter(userid=reg)
            
            for option_id in option:
                if (opt := Options.objects.filter(id=option_id, is_deleted=False)).exists():
                    options = opt.latest('id')

                    for record in record_list:
                        record.option = options
                        record.save()
                            
           
              
        
            response_data={
                "StatusCode":6000,
                "data":{
                    "title":"Success",
                    "Message":"Updated Successfully"
                }
            }
        
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"User Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_studentprofile(request,pk):
    if(reg:=StudentProfile.objects.filter(pk=pk,is_deleted=False)).exists():
        register=reg.latest('id')
        register.is_deleted=True
        register.save()
        response_data={
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['GET'])
@permission_classes([AllowAny])
def list_studentdetails(request,pk):
     if (student:=StudentProfile.objects.filter(pk=pk,is_deleted=False)).exists():
          serialized_data=StudentProfileSerializer(student,
                                                   context={
                                                        "request":request,
                                                   },many=True,).data
          response_data={
               "StatusCode":6000,
               "data":serialized_data
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})

@api_view(['GET'])
@permission_classes([AllowAny])
def list_studentprofile(request,pk):
     record=RecordAnswer.objects.filter(userid=pk,is_deleted=False).order_by('id')
     if record.exists():
          serialized_data=RecordAnswerSerializer(record,
                                                 context={
                                                      'request':request,
                                                 },
                                                 many=True,).data
          response_data={
               "StatusCode":6000,
               "data":serialized_data
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def update_selected_option(request,pk):
    name=request.data.get('name')
    email=request.data.get('email')
    mobile=request.data.get('mobile')
    dob=request.data.get('dob')
    
    record_answer=request.data.get('updated_records')
    if record_answer:
        for i in record_answer:
            id=i['recordid']
            value=i['updated_value']
            if (recordanswer:=RecordAnswer.objects.filter(userid=pk,id=id,is_deleted=False)).exists():
                    for i in record_answer:
                        id=i['recordid']
                        value=i['updated_value']
                        if (options:=RecordAnswer.objects.filter(pk=id,is_deleted=False)).exists():
                            option = options.latest("id")
                            if option:
                                new_option1 = Options.objects.get(id=value)
                                option.option=new_option1
                                option.save()
                    response_data={
                        "StatusCode":6000,
                        "data":{
                                "title":"Success",
                                "Message":"Updated Successfully"
                            }
                    }
                
            else:
                    response_data={
                        "StatusCode":6001,
                        "data":{
                            "title":"Failed",
                            "Message":"Not Found"
                        }
                }
    else:
        response_data={
                  "StatusCode":6001,
                  "data":{
                       "title":"Failed",
                       "Message":"Not Found"
                  }
             }
    return Response({'app_data':response_data})
                    
 
@api_view(['POST'])
@permission_classes([AllowAny])
def login_email(request):
    email=request.data.get('email')
    if StudentProfile.objects.filter(email=email,is_deleted=False).exists():
        student=StudentProfile.objects.filter(email=email,is_deleted=False)
        otp = generate_otp()
        send_otp_email(email, otp)
        user=CustomUser.objects.create(email=email,otp=otp)
        response_data={
             "StatusCode":6000,
             "data":{
                  "title":"Success",
                  "message": "OTP has been sent to your email"
             }
        }
    else:
        response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"User with this email does not exist"
              }
         }
    return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_otp(request):
    email = request.data.get('email', '')
    otp = request.data.get('otp')
    if StudentProfile.objects.filter(email=email, is_deleted=False).exists():
        student_profile = StudentProfile.objects.get(email=email, is_deleted=False)
        ss = CustomUser.objects.get(email=email)
        otpp = ss.otp
        if otpp == otp:
            headers = {
                "Content-Type": "application/json"
            }
            username = student_profile.username
            password = student_profile.password
            data = {
                "username": username,
                "password": password,
            }
            protocol = "http://"
            if request.is_secure():
                protocol = "https://"

            host = request.get_host()

            url = protocol + host + "/api/token/"
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                response = response.json()

                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "message": "Login successfully.",
                        "access_token": response["access"],
                        "refresh_token": response["refresh"],
                        "userid": student_profile.id
                    }
                }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Failed",
                        "message": "Token generation failed."
                    }
                }
        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "message": "Invalid OTP"
                },
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed!",
                "message": "User Not found"
            },
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
     serialized_data=LoginSerializer(data=request.data)
     if serialized_data.is_valid():
        mobile=request.data['mobile']
        country_code=request.data['country_code']
        if StudentProfile.objects.filter(country_code=country_code,mobile=mobile,is_deleted=False).exists():
             student_profile=StudentProfile.objects.get(country_code=country_code,mobile=mobile,is_deleted=False) 
             print(student_profile,'daxo')
             headers = {
                    "Content-Type": "application/json"
                }
             username = student_profile.username
             password = student_profile.password
             data = {
                    "username": username,
                    "password": password,
                }
             protocol = "http://"
             if request.is_secure():
                    protocol = "https://"

             host = request.get_host()

             url = protocol + host + "/api/token/"
             response = requests.post(url, headers=headers, data=json.dumps(data))
             if response.status_code == 200:
                    response = response.json()

                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Success",
                            "message": "Login successfully.",
                            # "phone": mobile,
                            "access_token" : response["access"],
                            "refresh_token" : response["refresh"],
                            "userid":student_profile.id
                        }
                    }
             else:
                    response_data = {
                        "StatusCode": 6001,
                        "data": {
                            "title": "Failed",
                            "message": "Token generation failed."
                        }
                    }
        else:
                
                response_data = {
                    "StatusCode": 6001,
                    "data" : {
                        "title": "Failed!",
                        "message": "User Not found"
                    },
                }
     else:
            response_data = {
                "StatusCode": 6001,
                "data" : {
                    "title": "Validation Error",
                    "message": generate_serializer_errors(serialized_data._errors)
                },
            }

     return Response({'app_data' : response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_student_review(request,pk):
        name=request.POST['name']
        rating=request.POST['rating']
        review=request.POST['review']
        if (university_data:=University.objects.filter(pk=pk,is_deleted=False)).exists():
            university=university_data.latest('id')
            student_review=ReviewStudent.objects.create(university=university,
                                                        name=name,
                                                        rating=rating,
                                                        review=review)
            response_data={
                "StatusCode":6000,
                "data":{
                        "title":"Success",
                        "Message":"Added Successfully"
                }
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                        "title":"Failed",
                        "Message":"Not Found"
                }
            }
        return Response({'app_data':response_data})
     

@api_view(['GET'])
@permission_classes([AllowAny])
def list_student_review(request,pk):
     if (student:=ReviewStudent.objects.filter(university=pk,is_deleted=False)).exists():
          serialized_data=ReviewStudentSerializer(student,
                                        context={
                                             "request":request,
                                        },
                                        many=True,).data
          response_data={
               "StatusCode":6000,
               "data":serialized_data
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_register_student(request):
    studentprofile = StudentProfile.objects.all()
    if studentprofile.exists():
        studentprofile.update(is_deleted=True)
        response_data={
            "Statuscode":6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def add_answer(request):
    userid = request.data.get('userid')
    question_id = request.data.getlist('question_id')
    try:
        selected_options = request.data.getlist('option')
    except:
        selected_options = None

    if (reg := StudentProfile.objects.filter(id=userid, is_deleted=False)).exists():
        user = reg.latest('id')

        records = []

        for q_id in question_id:
            if (q := Questions.objects.filter(id=q_id, is_deleted=False)).exists():
                qs = q.latest('id')
                for option_id in selected_options:
                    if (opt := Options.objects.filter(id=option_id, question=qs, is_deleted=False)).exists():
                        option_instance = opt.latest('id')
                        if (existing_record:= RecordAnswer.objects.filter(userid=user,option__question_id=qs)).exists():
                            existing_record=existing_record.latest('id')
                            existing_record.option = option_instance
                            existing_record.save()
                        else:
                                record = RecordAnswer.objects.create(userid=user, option=option_instance)
                                records.append(record)
                    else:
                        response_data = {
                            "StatusCode": 6002,
                            "data": {
                                "title": "Failed",
                                "Message": f"Option with ID {option_id} not found"
                            }
                        }
            else:
                  response_data = {
                            "StatusCode": 6002,
                            "data": {
                                "title": "Failed",
                                "Message": "Question Not Found"
                            }
                        }
                 

        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "Message": "Added Successfully",

            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "Message": "User Not Found"
            }
        }
    return Response({'app_data': response_data})


class StudentsAddAnswerAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_id = request.data.get('user_id')
        answers = request.data.get('answers')
        try:
            student_instance = StudentProfile.objects.get(id=user_id, is_deleted=False)
        except StudentProfile.DoesNotExist:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": "User Not Found"
                }
            }
            return Response({'app_data': response_data})
        try:
            with transaction.atomic():
                RecordAnswer.objects.filter(userid=student_instance.id).delete()

                for option_id in answers:
                    options_instance = Options.objects.filter(id=option_id).first()
                    RecordAnswer.objects.create(userid=student_instance, option=options_instance)

                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "Message": "Updated"
                    }
                }
        except Exception as e:
            print(e)
            response_data = {
                "StatusCode": 6002,
                "data": {
                    "title": "Failed",
                    "Message": "An error occurred"
                }
            }
        return Response({'app_data': response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def filter_university(request):
        try:
            userid=request.query_params.get('userid')
            coursetype=request.query_params.get('coursetype')
            course=request.query_params.get('course')
            country=request.query_params.get('country')
            specialization=request.query_params.get('specialization')
            if (reg:=StudentProfile.objects.filter(id=userid,is_deleted=False)).exists():
                user=reg.latest('id')
                universities_data=[]
                option=RecordAnswer.objects.filter(userid=user)
                
                if specialization:
                        for option_id in option:
                        # co=Specialization.objects.filter(id=specialization,course__course_name=course)
                        # c=co.latest('id')
                        # if c:
                            universities = University.objects.filter(options=option_id.option,service__coursetype=coursetype,specialization__course__course_name=course,country__in=country,specialization__specialization_name=specialization)
                            
                        
                            serialized_data=UniversitylistSpecializationSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            "specialization":specialization,
                                                            "userid":userid,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []


                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                     
                        response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
                else:
                    for option_id in option:
                            
                            universities = University.objects.filter(options=option_id.option,service__coursetype=coursetype,course__course_name=course,country__in=country)
                            if not universities:
                                universities = University.objects.filter(options=option_id.option)

                        
                            serialized_data=UniversitylistSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            "userid":userid,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []


                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                            
                            
                    
                    response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
            else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"User Not Found"  
                    }
                }
            
        except Exception as e:
            transaction.rollback()
            errType = e.__class__.__name__
            errors = {
                errType: traceback.format_exc()
            }
            response_data = {
                "status": 0,
                "api": request.get_full_path(),
                "request": request.data,
                "message": str(e),
                "response": errors
            }
        
        return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def suggest_filter_university(request):
        try:
            course=request.data.get('course')
            service=request.data.get('service')
            specialization=request.data.get('specialization')
            option=request.data.getlist('option')
            userid=request.data.get('userid')
            if (reg:=StudentProfile.objects.filter(id=userid,is_deleted=False)).exists():
                user=reg.latest('id')
                universities_data=[]
                if specialization:
                            for option_id in option:
                                universities = University.objects.filter(options=option_id,service=service,specialization__course__course_name=course,specialization__specialization_name=specialization)
                                
                            
                                serialized_data=UniversitylistSpecializationSerializer(universities,
                                                            context={
                                                                "course_name" : course,
                                                                "specialization":specialization,
                                                                "userid":userid,
                                                                'request':request,
                                                            },many=True,).data
                                universities_data.extend(serialized_data)
                                
                                unique_universities_list = []


                                for university in universities_data:
                                        if university not in unique_universities_list:
                                            unique_universities_list.append(university)
                            
                            response_data={
                                "StatusCode":6000,
                                "data":{
                                    "universities":unique_universities_list,
                                }
                            }
                else:
                    for option_id in option:
                        
                            universities = University.objects.filter(options=option_id,service=service,course__course_name=course)
                            
                        
                            serialized_data=UniversitylistSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            "userid":userid,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []


                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                            
                            
                    
                    response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
            else:
                 response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Student not found"
                    }
                 }
                
        except Exception as e:
            transaction.rollback()
            errType = e.__class__.__name__
            errors = {
                errType: traceback.format_exc()
            }
            response_data = {
                "status": 0,
                "api": request.get_full_path(),
                "request": request.data,
                "message": str(e),
                "response": errors
            }
        
        return Response({'app_data':response_data})



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_answer(request):
    if (answer:=RecordAnswer.objects.filter(is_deleted=False)).exists():
        serialized_data=RecordAnswerSerializer(answer,
                                               context={
                                                   "request":request,
                                               },
                                               many=True,).data
        response_data={
            "StatusCode":6000,
            "data":serialized_data
        }
    else:
        response_data={
            "data":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_answer(request,id):
    if (answer:=RecordAnswer.objects.filter(id=id,is_deleted=False)).exists():
        record=answer.latest('id')
        record.is_deleted=True
        record.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Success"
            }
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def add_student_record(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateStudentRecordSerializer(data=request.data)
        if serialized_data.is_valid():
            try:
                student_id = request.data['student']
                course_id = request.data['course']
                university_id=request.data['university']
                grade_10_certificate = request.data.get('grade_10_certificate')
                grade_12_certificate = request.data.get('grade_12_certificate')
                passport = request.data.get('passport')
                visa = request.data.get('visa')
                personal_id = request.data.get('personal_id')
                degree_certificate = request.data.get('degree_certificate')
            except:
                grade_10_certificate = None
                grade_12_certificate = None
                passport = None
                visa = None

            if not StudentRecord.objects.filter(student__id=student_id, course__id=course_id,university=university_id, is_deleted=False).exists():

                if (student := StudentProfile.objects.filter(id=student_id, is_deleted=False)).exists():
                    student = student.latest('id')
                    if (u:=University.objects.filter(id=university_id,is_deleted=False)).exists():
                        university=u.latest('id')
                        if (course := Course.objects.filter(id=course_id, is_deleted=False)).exists():
                            course = course.latest('id')

                            record = StudentRecord.objects.create(
                                student = student,
                                course = course,
                                university = university,
                                grade_10_certificate = grade_10_certificate,
                                grade_12_certificate = grade_12_certificate,
                                passport = passport,
                                visa = visa,
                                personal_id = personal_id,
                                degree_certificate = degree_certificate  
                            )

                            transaction.commit()
                            response_data = {
                                "StatusCode": 6000,
                                "data": {
                                    "title": "Success",
                                    "Message": "Added Successfully"
                                }
                            }
                        else:
                            response_data = {
                                "StatusCode" : 6001,
                                "data" : {
                                    "title" : "Failed",
                                    "message" : "Course not found"
                                }
                            }
                    else:
                            response_data = {
                                "StatusCode" : 6001,
                                "data" : {
                                    "title" : "Failed",
                                    "message" : "University not found"
                                }
                            }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Student not found"
                        }
                    }
            else:
                        s_record=request.data.get('record_id')
        
                        if (s:=StudentRecord.objects.filter(id=s_record,is_deleted=False)).exists():
                            student_record=s.latest('id')
                            if grade_10_certificate:
                                student_record.grade_10_certificate = grade_10_certificate
                            if grade_12_certificate:
                                student_record.grade_12_certificate  = grade_12_certificate
                            if passport:
                                student_record.passport = passport
                            if visa:
                                student_record.visa = visa
                            if personal_id:
                                student_record.personal_id = personal_id
                            if degree_certificate:
                                student_record.degree_certificate = degree_certificate

                            student_record.save()
                            
                            transaction.commit()
                            response_data = {
                                "StatusCode" : 6000,
                                "data" : {
                                    "title" : "Success",
                                    "message" : "Updated Successfully"
                                }
                            }
                        else:
                             response_data = {
                                    "StatusCode" : 6001,
                                    "data" : {
                                        "title" : "Failed",
                                        "message" : "Student not found"
                                    }
                                }
           
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def edit_student_record(request, pk):
    try:
        transaction.set_autocommit(False)
        grade_10_certificate = request.data.get('grade_10_certificate')
        grade_12_certificate = request.data.get('grade_12_certificate')
        passport = request.data.get('passport')
        visa = request.data.get('visa')
        personal_id = request.data.get('personal_id')
        degree_certificate = request.data.get('degree_certificate')

        if (student_record := StudentRecord.objects.filter(pk=pk, is_deleted=False)).exists():
            student_record = student_record.latest("id")

            if grade_10_certificate:
                student_record.grade_10_certificate = grade_10_certificate
            if grade_12_certificate:
                student_record.grade_12_certificate = grade_12_certificate
            if passport:
                student_record.passport = passport
            if visa:
                student_record.visa = visa
            if personal_id:
                student_record.personal_id = personal_id
            if degree_certificate:
                student_record.degree_certificate = degree_certificate

            student_record.save()

            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Updated Successfully"
                }
            }

        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message": "Student record not found"
                }
            }

    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_student_documents(request):
    student=request.GET.get('student')
    university=request.GET.get('university')
    if (student:=StudentRecord.objects.filter(student=student,university=university,is_deleted=False)).exists():
          serialized_data=StudentDocumentSerializer(student,
                                                  context={
                                                       "request":request,
                                                  },many=True,).data
          response_data={
               "StatusCode":6000,
               "data":serialized_data
          }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_student_record(request):
    student=request.GET.get('student')
    student_record=StudentRecord.objects.filter(student=student,is_deleted=False)
    if student_record.exists():
        serialized_data=StudentRecordSerializer(student_record,
                                                  context={
                                                       "request":request,
                                                  },many=True,).data
        notification_record = student_record.filter(is_read=True, is_deleted=False)
        if notification_record.exists():
            notification_record.update(notification=True)
            notification_status = True
        else:
            notification_status = False

          
        response_data={
               "StatusCode":6000,
               "data":serialized_data,
               "Notification":notification_status
          }
    else:
         
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})
    
@api_view(['POST'])
@permission_classes([AllowAny])
def notification_status(request,pk):
     university=request.data.get('university')
     if (student:=StudentRecord.objects.filter(student=pk,university=university)).exists():
          student=student.latest('id')
          student.notification=False
          student.is_read=False
          student.save()
          response_data={
               "StatusCode":6000,
               "data":{
                    "title":"Success",
                    "Message":"Notification updated"
               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":
               {
                "title":"Failed",
               "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_student_record(request):
    total_applications=StudentRecord.objects.filter(is_deleted=False).count()
    pending_applications=StudentRecord.objects.filter(is_deleted=False,status="pending").count()
    approved_applications=StudentRecord.objects.filter(is_deleted=False,status="approved").count()
    rejected_applications=StudentRecord.objects.filter(is_deleted=False,status="rejected").count()
    q=request.GET.get('q')
    record=StudentRecord.objects.filter(is_deleted=False)
    if record:
        if q:
            std = record.filter(
                    Q(status__icontains=q) | 
                    Q(course__course_name__icontains=q) 
                    
                )
        
            serialized_data=StudentRecordViewSerializer(std,
                                                    context={
                                                        "request":request,
                                                    },many=True).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "total_applications":total_applications,
                "pending_applications":pending_applications,
                "approved_applications":approved_applications,
                "rejected_applications":rejected_applications,
            }
       
        else:  
       
            serialized_data=StudentRecordViewSerializer(record,
                                                    context={
                                                        "request":request,
                                                    },many=True).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "total_applications":total_applications,
                "pending_applications":pending_applications,
                "approved_applications":approved_applications,
                "rejected_applications":rejected_applications,
            }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})
        
   
@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_student_record(request,pk):
    record=StudentRecord.objects.filter(student=pk,is_deleted=False)
    if record:
        serialized_data=StudentSingleRecordViewSerializer(record,
                                                context={
                                                    "request":request,
                                                },many=True).data
        response_data={
            "StatusCode":6000,
            "data":serialized_data
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                 "title":"Failed",
                 "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def update_university_status_approved(request,id):
    if (student:=StudentRecord.objects.filter(id=id,status="pending",is_deleted=False)).exists():
         student=student.latest('id')
         student.status="approved"
         student.is_read=True
         student.save()
         response_data={
              "StatusCode":6000,
              "data":{
                   "title":"Success",
                   "Message":"Status Updated"
              }
         }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def update_university_status_rejected(request,id):
    if (student:=StudentRecord.objects.filter(id=id,status="pending",is_deleted=False)).exists():
         student=student.latest('id')
         student.status="rejected"
         student.save()
         response_data={
              "StatusCode":6000,
              "data":{
                   "title":"Success",
                   "Message":"Status Updated"
              }
         }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_student_record(request):
    record=StudentRecord.objects.all()
    if record.exists():
         record.update(is_deleted=True)
         response_data={
            "Statuscode":6000,
            "data":{
                 "title":"Success",
                 "Message":"Deleted Successfully"
            }
         }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                "title":"Failed",
                "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})




@api_view(['POST'])
@permission_classes([AllowAny])
def add_wishlist(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddWishListSerializer(data=request.data)
        if serialized_data.is_valid():
            student_id = request.data["student"]
            university_id = request.data["university"]
            course_id=request.data["course"]
            if (university := University.objects.filter(pk=university_id, is_deleted=False)).exists():
                university = university.latest('id')
                if (course:= Course.objects.filter(pk=course_id,is_deleted=False)).exists():
                    course=course.latest('id')
                    if (student := StudentProfile.objects.filter(pk=student_id, is_deleted=False)).exists():
                        student = student.latest('id')
                        if not StudentWishList.objects.filter(student=student,university=university,is_active=True, is_deleted=False).exists():

                            wish_list = StudentWishList.objects.create(
                                student = student,
                                university = university,
                                course=course,
                                is_active=True
                            )

                            transaction.commit()
                            response_data = {
                                "StatusCode": 6000,
                                "data": {
                                    "title": "Success",
                                    "Message": "Added Successfully"
                                }
                            }
                        else:
                            response_data = {
                                "StatusCode": 6001,
                                "data": {
                                    "title": "Failed",
                                    "Message": "university already added to wishlist "
                                }
                            }
                             
                    else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Student not found"
                            }
                        }
                else:
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Course not found"
                            }
                        }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Failed",
                        "Message": "University Not Found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }


    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_wishlist(request):
    try:
        student_id = request.GET.get('student_id')
        if (wishlist := StudentWishList.objects.filter(student__id=student_id, is_deleted=False)).exists():
            serialized_data = StudentWishListSerializer(
            wishlist,
            context={
                "request": request,
            },
            many=True,
            ).data
            response_data = {
                "StatusCode": 6000,
                "data": serialized_data
            }
        else:
             response_data = {
                  "StatusCode" : 6001,
                  "data" : []
             }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def remove_wishlist(request):
    university=request.data.get('university')
    student=request.data.get('student')
    if (student:=StudentWishList.objects.filter(university=university,student=student,is_deleted=False)).exists():
        student=student.latest('id')
        student.is_active=False
        student.is_deleted=True
        student.save()
        response_data={
             "StatusCode":6000,
             "data":{
                  "title":"Success",
                  "Message":"Removed from wishlist"
             }
        }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":"Not Found"
              }
         }
    return Response({'app_data':response_data})
     

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def count_enquiry(request):
     if (std:=StudentProfile.objects.filter(is_deleted=False)).exists():
          std=StudentProfile.objects.filter(is_deleted=False).count()
          enq=Enquiry.objects.filter(is_deleted=False).count()
          app=StudentRecord.objects.filter(is_deleted=False).count()
          response_data={
               "StatusCode":6000,
               "data":{
                    "Enquiry_count":enq,
                    "Registered_student":std,
                    "Student_Application":app

               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def count_student_record(request):
     if (count:=StudentRecord.objects.filter(is_deleted=False)).exists():
          count=StudentRecord.objects.filter(is_deleted=False).count()
          response_data={
               "StatusCode":6000,
               "data":{
                    "pending_student_record":count
               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def count_completed_student(request):
     if (count:=StudentRecord.objects.filter(is_deleted=False,status="approved")).exists():
          count=StudentRecord.objects.filter(is_deleted=False,status="approved").count()
          response_data={
               "StatusCode":6000,
               "data":{
                    
                         "completed_student_count":count
                    
               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def count_pending_application(request):
     if (count:=StudentRecord.objects.filter(is_deleted=False,status="pending")).exists():
          count=StudentRecord.objects.filter(is_deleted=False,status="pending").count()
          response_data={
               "StatusCode":6000,
               "data":{
                    
                         "pending_application_count":count
                    
               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def count_rejected_application(request):
     if (count:=StudentRecord.objects.filter(is_deleted=False,status="rejected")).exists():
          count=StudentRecord.objects.filter(is_deleted=False,status="rejected").count()
          response_data={
               "StatusCode":6000,
               "data":{
                    
                         "completed_student_count":count
                    
               }
          }
     else:
          response_data={
               "StatusCode":6001,
               "data":{
                    "title":"Failed",
                    "Message":"Not Found"
               }
          }
     return Response({'app_data':response_data})    

@api_view(['GET'])
@permission_classes([AllowAny])
def specialization_filter_university(request):
        try:
            userid=request.query_params.get('userid')
            coursetype=request.query_params.get('coursetype')
            course=request.query_params.get('course')
            country=request.query_params.get('country')
            specialization=request.query_params.get('specialization')
            if (reg:=StudentProfile.objects.filter(id=userid,is_deleted=False)).exists():
                user=reg.latest('id')
                universities_data=[]
                option=RecordAnswer.objects.filter(userid=user)
                
                if specialization:
                    for option_id in option:
                    
                            universities = University.objects.filter(options=option_id.option,service__coursetype=coursetype,specialization__course__course_name=course,country__in=country,specialization__specialization_name=specialization)
                        
                            serialized_data=UniversitylistSpecializationSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            "specialization":specialization,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []


                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                     
                    response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
               
                    
            else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"User Not Found"  
                    }
                }
            
        except Exception as e:
            transaction.rollback()
            errType = e.__class__.__name__
            errors = {
                errType: traceback.format_exc()
            }
            response_data = {
                "status": 0,
                "api": request.get_full_path(),
                "request": request.data,
                "message": str(e),
                "response": errors
            }        
        return Response({'app_data':response_data})
    



@api_view(['POST'])
@permission_classes([AllowAny])
def add_enquiry(request):
  try:
    serialized_data=AddEnquirySerializer(data=request.data)
    if serialized_data.is_valid():
        name=request.data['name']
        last_name=request.data.get('last_name')
        email=request.data.get('email')
        phone=request.data['phone']
        message=request.data.get('message')
        enquiry=Enquiry.objects.create(name=name,
                                       last_name=last_name,
                                       email=email,
                                       phone=phone,
                                       message=message
                                     )
       
        context = {'name':name,'last_name':last_name,'email':email,'phone':phone,'message':message}
        template = get_template('index2.html').render(context)
        e=settings.EMAIL_HOST_USER
        send_mail(
                     'Enquiry Data',
                     None, # Pass None because it's a HTML mail
                     settings.EMAIL_HOST_USER,
                     [e],
                     fail_silently=False,
                     html_message = template,
                      )
            
        response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : " added successfully"
                    }
                }            
    else:
             response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : generate_serializer_errors(serialized_data._errors)
                    }
                }
    return Response({'app_data' : response_data})
    
  except Exception as E:
    print(E)
    return Response({'app_data' : 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# class
@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_enquiry(request):
    if (enquiry:=Enquiry.objects.filter(is_deleted=False)).exists():
        enq = Enquiry.objects.filter(is_deleted=False).order_by('is_read','-enquiry_date')
        count=Enquiry.objects.filter(is_deleted=False).count()
        is_read_count=Enquiry.objects.filter(is_read=False).count()
        q=request.GET.get('q')
        if q:
            std = enq.filter(
            Q(name__icontains=q) | 
            Q(last_name__icontains=q)   
            )
            serialized_data=EnquirySerializer(std,
                                            context={
                                                "request":request,
                                            },many=True,).data
        else:
            serialized_data=EnquirySerializer(enq,
                                context={
                                    "request":request,
                                },many=True,).data
        response_data={
            "StatusCode":6000,
            "data":serialized_data,
            "Count":count,
            "Is_read_count":is_read_count
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_enquiry(request,id):
    if (enquiry:=Enquiry.objects.filter(id=id,is_deleted=False)).exists():
        enquiry=enquiry.latest('id')
        enquiry.is_deleted=True
        enquiry.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def enquiry_read(request,id):
          if (e:=Enquiry.objects.filter(id=id,is_deleted=False)).exists():
              enq=e.latest('id')
              enq.is_read=True
              enq.save()

              response_data={
                    "StatusCode" : 6000,
                     "data":{
                            "title": "Success",
                            "message":" Updated"
                     }
              }
          else:
              response_data={
                    "StatusCode" : 6001,
                     "data":{
                            "title":"Failed",
                            "message":"Not found"
                     }
              }
          return Response(response_data)



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def admin_add_student(request):
    serialized_data=AddStudentProfileSerializer(data=request.data)
    if serialized_data.is_valid():
        name=request.data.get('name')
        email=request.data.get('email')
        mobile=request.data.get('mobile')
        student=StudentProfile.objects.create(name=name,
                               email=email,
                               mobile=mobile)
        response_data={
            "StatusCode":6000,
            "data":{
                 "title":"Success",
                 "Message":"Added Successfully"
            }
        }
    else:
         response_data={
              "StatusCode":6001,
              "data":{
                   "title":"Failed",
                   "Message":generate_serializer_errors(serialized_data._errors)
              }
         }
    return Response({'app_data':response_data})
        

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def admin_add_answer(request):
    userid = request.data.get('userid')
    question_id = request.data.getlist('question_id')
    try:
        selected_options = request.data.getlist('option')
    except:
        selected_options = None

    if (reg := StudentProfile.objects.filter(id=userid, is_deleted=False)).exists():
        user = reg.latest('id')

        records = []

        for q_id in question_id:
            if (q := Questions.objects.filter(id=q_id, is_deleted=False)).exists():
                qs = q.latest('id')
                for option_id in selected_options:
                    if (opt := Options.objects.filter(id=option_id, question=qs, is_deleted=False)).exists():
                        option_instance = opt.latest('id')
                        if (existing_record:= RecordAnswer.objects.filter(userid=user,option__question_id=qs)).exists():
                            existing_record=existing_record.latest('id')
                            existing_record.option = option_instance
                            existing_record.save()
                        else:
                                record = RecordAnswer.objects.create(userid=user, option=option_instance)
                                records.append(record)
                    else:
                        response_data = {
                            "StatusCode": 6002,
                            "data": {
                                "title": "Failed",
                                "Message": f"Option with ID {option_id} not found"
                            }
                        }
            else:
                  response_data = {
                            "StatusCode": 6002,
                            "data": {
                                "title": "Failed",
                                "Message": "Question Not Found"
                            }
                        }
                 

        response_data = {
            "StatusCode": 6000,
            "data": {
                "title": "Success",
                "Message": "Added Successfully",

            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "Message": "User Not Found"
            }
        }
    return Response({'app_data': response_data})
          
          
@api_view(['GET'])
@permission_classes([AllowAny])
def admin_filter_university(request):
        try:
            userid=request.query_params.get('userid')
            coursetype=request.query_params.get('coursetype')
            course=request.query_params.get('course')
            country=request.query_params.get('country')
            specialization=request.query_params.get('specialization')
            if (reg:=StudentProfile.objects.filter(id=userid,is_deleted=False)).exists():
                user=reg.latest('id')
                universities_data=[]
                option=RecordAnswer.objects.filter(userid=user)
                
                if specialization:
                     for option_id in option:
                        co=Specialization.objects.filter(specialization_name=specialization,course__course_name=course)
                        c=co.latest('id')
                        if c:
                            universities = University.objects.filter(options=option_id.option,service__coursetype=coursetype,specialization__course__course_name=course,country__in=country,specialization__specialization_name=specialization)
                            
                        
                            serialized_data=UniversitylistSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []

                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                     
                        response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
                else:
                    for option_id in option:
                        
                            universities = University.objects.filter(options=option_id.option,service__coursetype=coursetype,course__course_name=course,country__in=country)
                            
                        
                            serialized_data=UniversitylistSerializer(universities,
                                                        context={
                                                            "course_name" : course,
                                                            'request':request,
                                                        },many=True,).data
                            universities_data.extend(serialized_data)
                            
                            unique_universities_list = []


                            for university in universities_data:
                                    if university not in unique_universities_list:
                                        unique_universities_list.append(university)
                            
                            
                    
                    response_data={
                            "StatusCode":6000,
                            "data":{
                                "universities":unique_universities_list,
                            }
                        }
            else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"User Not Found"  
                    }
                }
            
        except Exception as e:
            transaction.rollback()
            errType = e.__class__.__name__
            errors = {
                errType: traceback.format_exc()
            }
            response_data = {
                "status": 0,
                "api": request.get_full_path(),
                "request": request.data,
                "message": str(e),
                "response": errors
            }
        
        return Response({'app_data':response_data})   


class SuggestedCollageAPIView(APIView):
    # @group_required(['ezgrad_admin'])
    def post(self, request):
        data = request.data.copy()
        if 'profile_image' not in data or data['profile_image'] == "":
            data['profile_image'] = None
        serializer = SuggestionAddSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "Message": serializer.data
                }
            }
            return Response({'app_data':response_data})
        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": serializer.errors
                }
            }
            return Response({'app_data':response_data})
        
    def get(self, request,id=None):
        if id:
            try:
                instance = CollageSuggestion.objects.filter(id=id,is_deleted=False).first()
                serializer = SuggestionSerializer(instance, context={'request': self.request})
                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": serializer.data
                    }
                }
            except Exception as e:
                print(f"Error occurred: {e}")
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Error",
                        "Message": "An error occurred while processing your request."
                    }
                }
        else:
            try:
                instance = CollageSuggestion.objects.filter(is_deleted=False).order_by('-date')
                serializer = SuggestionSerializer(instance, many=True, context={'request': self.request})
                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": serializer.data
                    }
                }
            except Exception as e:
                print(f"Error occurred: {e}")
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Error",
                        "Message": "An error occurred while processing your request."
                    }
                }
        return Response({'app_data': response_data})

    def patch(self, request, id=None):
        instance = self.get_object(id)
        if not instance:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": "Id Not found"
                }
            }
            return Response({'app_data': response_data})
        else:
            data = request.data.copy()
            if 'profile_image' not in data or data['profile_image'] == "":
                data['profile_image'] = instance.profile_image
            serializer = SuggestionAddSerializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": serializer.data
                    }
                }
                return Response({'app_data': response_data}, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "StatusCode": 6002,
                    "data": {
                        "title": "Error",
                        "Message": serializer.errors
                    }
                }
                return Response({'app_data': response_data})

    def get_object(self, id):
        try:
            instance = CollageSuggestion.objects.filter(id=id, is_deleted=False).first()
            return instance
        except CollageSuggestion.DoesNotExist:
            return None

class GetUserSuggestData(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,id):
        instance = self.get_object(id)
        if not instance:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": "Id Not found"
                }
            }
            return Response({'app_data': response_data}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = SuggestionSerializer(instance,context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data
                }
            }
            return Response({'app_data': response_data})

    def get_object(self, id):
        try:
            instance = CollageSuggestion.objects.filter(id=id, is_deleted=False).first()
            return instance
        except CollageSuggestion.DoesNotExist:
            return None
        
class SIngleCollageInfo(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,id):
        instance = self.get_object(id)
        if not instance:
             response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": "Id Not found"
                }
            }
        else:
            serializer = SingleCollageInfo(instance,context={'request': self.request})
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data,
                    "Message": "Success"

                }
            }
        return Response({'app_data': response_data})

    def get_object(self,id):
        try:
            instance = University.objects.filter(id=id,is_deleted=False).first()
            return instance
        except Exception as e:
             print(e)
             return None
























# @csrf_exempt
# def UserLogin(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     if User.objects.filter(username=username,password=password).exists():
#         u = User.objects.get(username=username,password=password)
#         if u.last_name == 'User':
#             f = Register.objects.filter(user_id=u.id)
#             s = RegisterSerializer(f,many=True)
#             return Response({"message":"True","response":"success"})
            
#         else:
#             return Response({"message":"True","response":"Invalid Username or password"})
#     else:
#         return Response({"message":"True","response":"Not Found"})



