from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from student.models import RecordAnswer,StudentProfile,StudentRecord
from course.models import University,Facts,CurrencySymbol,Course,AlumniTalk,States,UniversityImages,UniversityDocuments,Specialization,Accreditation,AccreditationPoints,AdmissionProcedures,Facilities,FacilityType,Country,CourseSpecialization,Faq,PlacementPartners,UniversityBanner
from service.models import CourseType,ServiceType
from question.models import Options
from api.v1.service.serializers import ServiceSerializer
from api.v1.course.serializers import AddadmissionProcedureSerializer,AlumniTalkSerializer,AddUniversityImageSerializer,UniversityImageSerializer,SearchUniversitySerializer,SuggestCourseSerializer,SingleUniversityDetailsSerializer,CompareUniversitySerializer,StateSerializer,CourseStateSerializer,AddUniversityDocumentSerializer,UniversityDocumentSerializer,AddSpecializationSerializer,SpecializationSerializer,AccreditationSerializer,AccreditationPointSerializer,AddAccreditationSerializer,AddAccreditationPointsSerializer,AddcurrencySerializer,CurrencySerializer,ListCourseSpecializationUniversity,AdmissionProcedureSerializer,CourseCountrySerializer,PopularUniversitySerializer,FacilitiesSerializer,FacilityTypeSerializer,AddFacilitiesSerializer,AddFacilityTypeSerializer,UniversityBannerSerializer,AddUniversityBannerSerializer,AddFaqSerializer,AddCountrySerializer,AddCourseSpecializationSerializer,AddCourseSerializer,AddFactSerializer,AddUniversitySerializer,UniversitySerializer,PlacementPartnerSerializer,AddplacementpartnerSerializer,FactSerializer,CourseviewSerializer,FaqSerializer,CourseSerializer,CourseSpecializationSerializer,CountrySerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from general.functions import generate_serializer_errors
from general.decorators import group_required
from forex_python.converter import CurrencyRates
from rest_framework import status
import requests
import traceback
from django.db import transaction
from django.db.models import Q
from django.db.models import Max, Min, IntegerField
from django.db.models.functions import Cast
from question.models import *
from api.v1.question.serializers import *
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_university(request):
    serialized_data=AddUniversitySerializer(data=request.data)
    if serialized_data.is_valid():
        logo=request.data['university_logo']
        name=request.data['university_name']
        about=request.data['about_university']
        university_image=request.data.get('university_image')
        certificate=request.data.get('sample_certificate')
        prospectus=request.data.get('prospectus')
        service=request.data.get('service')
        country=request.data.getlist('country')
        state=request.data.getlist('state')
        option=request.data.getlist('option')
        approved_by=request.data.getlist('approved_by')
        student_choice=request.data.get('student_choice')
        student_review=request.data.get('student_review')
        credit_points=request.data.get('credits_points')
        world_ranking=request.data.get('world_ranking')
        e_learning_facility=request.data.get('e_learning_facility')
        country_ranking=request.data.get('country_ranking')
        placement_assistance=request.data.get('placement_assistance')
        industry_ready=request.data.get('industry_ready')
        satisfied_student=request.data.get('satisfied_student')
        pros=request.data.get('pros')
        nirf_training=request.data.get('nirf_training')
        wes_approval=request.data.get('wes_approval')
        slug=request.data['slug']
        renamed_slug=slug.replace(' ','-')
        if (s:=ServiceType.objects.filter(id=service)).exists():
            services=s.latest('id')
            if (p:=University.objects.filter(is_deleted=False,slug=renamed_slug)).exists():
                   response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Slug Already Exist"
                    }
                }
            else:
                university=University.objects.create(service=services,
                                                university_logo=logo,
                                                university_image=university_image,
                                                university_name=name,
                                                about_university=about,
                                                sample_certificate=certificate,
                                                prospectus=prospectus,
                                                student_choice=student_choice,
                                                student_review=student_review,
                                                credit_points=credit_points,
                                                world_ranking=world_ranking,
                                                e_learning_facility=e_learning_facility,
                                                country_ranking=country_ranking,
                                                placement_assistance=placement_assistance,
                                                industry_ready=industry_ready,
                                                satisfied_student=satisfied_student,
                                                pros=pros,
                                                nirf_training=nirf_training,
                                                wes_approval=wes_approval,
                                                slug=renamed_slug
                                                )
                country_obj=country
                for i in country_obj:
                    countries=Country.objects.get(id=i)
                university_obj=university.country.add(countries)
                state_obj=state
                for i in state_obj:
                    states=States.objects.get(id=i)
                u_obj=university.state.add(states)
                option_obj=option
                for i in option_obj:
                    options=Options.objects.get(id=i)
                options_obj=university.options.add(options)
                approved_by_obj=approved_by
                for i in approved_by_obj:
                    approved_by=Accreditation.objects.get(id=i)
                approved=university.approved_by.add(approved_by)

                response_data={
                    "StatusCode":6000,
                    "data":{
                        "title":"Success",
                        "Message":"Successfully added"
                    }
                }
        else:
            response_data={
                "StatusCode":6000,
                "data":{
                    "title":"Failed",
                    "Message":"Service Not Found"
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_university(request):
    if (university:=University.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversitySerializer(university,
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


@api_view(['GET'])
# @group_required(['ezgrad_admin'])
@permission_classes([AllowAny])
def view_single_university(request,pk):
    if (university:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        serialized_data=UniversitySerializer(university,
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



@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_university(request,pk):
    logo=request.data.get('university_logo')
    university_image=request.data.get('university_image')
    name=request.data.get('university_name')
    about=request.data.get('about_university')
    certificate=request.data.get('sample_certificate')
    prospectus=request.data.get('prospectus')
    country=request.data.getlist('country')
    state=request.data.getlist('state')
    option=request.data.getlist('option')
    approved_by=request.data.getlist('approved_by')
    student_choice=request.data.get('student_choice')
    student_review=request.data.get('student_review')
    credit_points=request.data.get('credit_points')
    world_ranking=request.data.get('world_ranking')
    e_learning_facility=request.data.get('e_learning_facility')
    country_ranking=request.data.get('country_ranking')
    placement_assistance=request.data.get('placement_assistance')
    industry_ready=request.data.get('industry_ready')
    satisfied_student=request.data.get('satisfied_student')
    pros=request.data.get('pros')
    nirf_training=request.data.get('nirf_training')
    wes_approval=request.data.get('wes_approval')
    rating=request.data.get('rating')
    slug=request.data.get('slug')

    if (u:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        university=u.latest('id')
        if logo:
            university.university_logo=logo
        if university_image:
            university.university_image=university_image
        if name:
            university.university_name=name
        if about:
            university.about_university=about
        if certificate:
            university.sample_certificate=certificate
        if prospectus:
            university.prospectus=prospectus
        if student_choice:
            university.student_choice=student_choice
        if student_review:
            university.student_review=student_review
        if credit_points:
            university.credit_points=credit_points
        if world_ranking:
            university.world_ranking=world_ranking
        if e_learning_facility:
            university.e_learning_facility=e_learning_facility
        if country_ranking:
            university.country_ranking=country_ranking
        if placement_assistance:
            university.placement_assistance=placement_assistance
        if industry_ready:
            university.industry_ready=industry_ready
        if satisfied_student:
            university.satisfied_student=satisfied_student
        if pros:
            university.pros=pros
        if nirf_training:
            university.nirf_training=nirf_training
        if wes_approval:
            university.wes_approval=wes_approval
        if rating:
            university.rating=rating
        if slug:
            renamed_slug=slug.replace(' ','-')
            if (p:=University.objects.filter(is_deleted=False,slug=renamed_slug)).exclude(id=university.id).exists():
                    response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                            "title" : "Failed",
                            "message" : "Slug Already Exist"
                    }
                    }
                    return Response(response_data)
            else:
                university.slug=renamed_slug
        if country:
            country_objects = Country.objects.filter(id__in=country)
            university.country.set(country_objects)
        if state:
            state_objects = States.objects.filter(id__in=state)
            university.state.set(state_objects)
        if option:
            option_objects = Options.objects.filter(id__in=option)
            university.options.set(option_objects)
        if approved_by:
            approved_by_objects = Accreditation.objects.filter(id__in=approved_by)
            university.approved_by.set(approved_by_objects)
        university.save()
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
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_university(request,pk):
    if (u:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        university=u.latest('id')
        university.is_deleted=True
        university.save()
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_universitylogo_studentform(request):
    service=request.query_params.get('service')
    country=request.query_params.getlist('country')
    coursename=request.query_params.get('coursename')
    specialization=request.query_params.get('specialization')
    if specialization:
        university = University.objects.filter(country__in=country,service=service,course__course_name=coursename,specialization__specialization_name=specialization).distinct('university_name')
        if university.exists():
            serialized_data=UniversitySerializer(university,
                                                context={
                                                    "request":request,
                                                },

                                                many=True,).data
            university_count=University.objects.filter(country__in=country,course__course_name=coursename,specialization__specialization_name=specialization).distinct('university_name').count()
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "count":university_count
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Not found"
                }
            }

    elif (university:=University.objects.filter(country__in=country,service=service,course__course_name=coursename)).exists():
        serialized_data=UniversitySerializer(university,
                                             context={
                                                 "request":request,
                                             },
                                             many=True,).data
        university_count=University.objects.filter(country__in=country,course__course_name=coursename).count()
        response_data={
            "StatusCode":6000,
            "data":serialized_data,
            "count":university_count
        }
    elif (university:=University.objects.filter(service=service,course__course_name=coursename)).exists():
        serialized_data=UniversitySerializer(university,
                                             context={
                                                 "request":request,
                                             },
                                             many=True,).data
        university_count=University.objects.filter(course__course_name=coursename).count()
        response_data={
            "StatusCode":6000,
            "data":serialized_data,
            "count":university_count
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
def list_course_studentform(request):
    course=request.query_params.get('course')
    service=request.query_params.get('service')
    coursetype=request.query_params.get('coursetype')
    country=request.query_params.getlist('country')
    state=request.query_params.getlist('state')
    if course and country and state:
        courses = Course.objects.filter(pk=course,university__country__in=country,university__state__in=state,course_type=coursetype,university__service=service)
        course_obj=Course.objects.filter(pk=course).first()
        # university=University.objects.filter(service__coursetype=coursetype,course__course_name=course,country__in=country)
        university_count=University.objects.filter(course__course_name=course_obj.course_name,course__university__country__states__in=state).count()
        if courses.exists():
            if len(state) > 1:
                course_data = Course.objects.filter(type="general",pk=course)
                serialized_data = CourseSerializer(course_data, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data
                }
            else:
                serialized_data = CourseSerializer(courses, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data,
                    "count":university_count
                }
        else:
            c = Course.objects.filter(pk=course,university__country__in=country,university__state__in=state,university__service=service)
            if c:
                serialized_data = CourseSerializer(c, context={"request": request}, many=True).data
                response_data = {
                        "StatusCode": 6000,
                        "data": serialized_data,
                        "count":university_count
                    }
            else:

                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Course Not Found"
                    }
                }
    elif course and country:
        courses = Course.objects.filter(pk=course,university__country__in=country,course_type=coursetype,university__service=service)
        course_obj=Course.objects.filter(pk=course).first()
        # university=University.objects.filter(service__coursetype=coursetype,course__course_name=course,country__in=country)
        university_count=University.objects.filter(course__course_name=course_obj.course_name,course__university__country__in=country).count()
        if courses.exists():
            if len(country) > 1:
                course_data = Course.objects.filter(type="general",pk=course)
                serialized_data = CourseSerializer(course_data, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data
                }
            else:
                serialized_data = CourseSerializer(courses, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data,
                    "count":university_count
                }

        else:
            c = Course.objects.filter(pk=course,university__country__in=country,university__service=service)
            if c:
                serialized_data = CourseSerializer(c, context={"request": request}, many=True).data
                response_data = {
                        "StatusCode": 6000,
                        "data": serialized_data,
                        "count":university_count
                    }
            else:

                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Course Not Found"
                    }
                }
    else:
         response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Country and course and State Not Found"
                }
            }
        
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_regular_course_studentform(request):
    course=request.query_params.get('course')
    service=request.query_params.get('service')
    coursetype=request.data.get('coursetype')
    country=request.query_params.getlist('country')
    state=request.query_params.getlist('state')
    if course and country:
        courses = Course.objects.filter(pk=course,university__country__states__in=state,course_type=coursetype,course_type__service_id=service)
        course_obj=Course.objects.filter(pk=course).first()
        # university=University.objects.filter(service__coursetype=coursetype,course__course_name=course,country__in=country)
        university_count=University.objects.filter(course__course_name=course_obj.course_name,course__university__country__states__in=state).count()
        if courses.exists():
            if len(country) > 1:
                course_data = Course.objects.filter(type="general",pk=course)
                serialized_data = CourseSerializer(course_data, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data
                }
            else:
                serialized_data = CourseSerializer(course_obj, context={"request": request}, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": serialized_data,
                    "count":university_count
                }

        else:
            c = Course.objects.filter(pk=course,university__country__in=country,university__service=service)
            if c:
                serialized_data = CourseSerializer(c, context={"request": request}, many=True).data
                response_data = {
                        "StatusCode": 6000,
                        "data": serialized_data,
                        "count":university_count
                    }
            else:

                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Course Not Found"
                    }
                }
    else:
         response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Country and course Not Found"
                }
            }
        
    return Response({'app_data':response_data})



@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_course(request):
    course = Course.objects.all()
    if course.exists():
        course.update(is_deleted=True)
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
@group_required(['ezgrad_admin'])
def add_admission_procedure(request):
    serialized_data=AddadmissionProcedureSerializer(data=request.data)
    if serialized_data.is_valid():
        points=request.data['points']
        course=request.data.get('course')
        specialization=request.data.get('specialization')
        if course:
            if (course_data:=Course.objects.filter(id=course,is_deleted=False)).exists():
                c=course_data.latest('id')
                course_admission_procedure=AdmissionProcedures.objects.create(course=c,
                                                                        points=points)
                response_data={
                    "StatusCode":6000,
                    "data":{
                        "title":"Success",
                        "Message":"Added Successfully"
                    }
                }
        elif specialization:
            if (specialization_data:=Specialization.objects.filter(id=specialization,is_deleted=False)).exists():
                s=specialization_data.latest('id')
                specialization_admission_procedure=AdmissionProcedures.objects.create(specialization=s,
                                                                        points=points)
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
@group_required(['ezgrad_admin'])
def view_admission_procedure(request,pk):
    if (admission:=AdmissionProcedures.objects.filter(course=pk,is_deleted=False)).exists():
        serialized_data=AdmissionProcedureSerializer(admission,
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
@group_required(['ezgrad_admin'])
def view_specialization_admission_procedure(request,pk):
    if (admission:=AdmissionProcedures.objects.filter(specialization=pk,is_deleted=False)).exists():
        serialized_data=AdmissionProcedureSerializer(admission,
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
@group_required(['ezgrad_admin'])
def view_single_admission_procedure(request,id):
    if (admission:=AdmissionProcedures.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=AdmissionProcedureSerializer(admission,
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_admission_procedure(request,id):
    points=request.data.get('points')
    if (a:=AdmissionProcedures.objects.filter(id=id,is_deleted=False)).exists():
        ad=a.latest('id')
        if points:
            ad.points=points
        ad.save()
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
    return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_admission_procedure(request,id):
    if (a:=AdmissionProcedures.objects.filter(id=id,is_deleted=False)).exists():
        ad=a.latest('id')
        ad.is_deleted=True
        ad.save()
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_all_courses(request):
    if (course:=Course.objects.filter(is_deleted=False).distinct('course_name')).exists():
        serialized_data=CourseviewSerializer(course,
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
def list_specialization_course_university(request):
    try:
        s=request.GET.get('specialization')
        course=request.GET.get('course')
        specializations= Specialization.objects.filter(course__course_name=course,specialization_name=s, is_deleted=False).distinct('specialization_name')
        if specializations.exists():
            serialized_data = ListCourseSpecializationUniversity(
                specializations,
                context={
                    "request": request,
                },
                many = True
            ).data

            min_value = Specialization.objects.filter(course__course_name=course, specialization_name=s, is_deleted=False).aggregate(min_value=Min('year_fee'))['min_value']
            max_value = Specialization.objects.filter(course__course_name=course, specialization_name=s, is_deleted=False).aggregate(max_value=Max('year_fee'))['max_value']
            
            response_data = {
                "StatusCode": 6000,
                "data": serialized_data,
                "min_value":min_value,
                "max_value":max_value,
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
    return Response({'app_data': response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_universities_specialization(request):
    try:
        specialization=request.GET.get('specialization')
        course=request.GET.get('course')
        universities = University.objects.filter(specialization__course__course_name=course,specialization__specialization_name=specialization)
        if universities.exists():
            serialized_data = ListCourseSpecializationUniversity(
                       universities,
                        context={
                            "request": request,
                        },
                    ).data
            universities.append(serialized_data)

            response_data = {
                "StatusCode": 6000,
                "data": universities,
            }
        else:
            response_data = {
                "StstusCode" : 6001,
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
    return Response({'app_data': response_data})




@api_view(['GET'])
@permission_classes([AllowAny])
def search_course(request):
    try:
        q =  request.GET.get('q')
        if (course := Course.objects.filter(is_deleted=False)).exists():

            if q:
                course = course.filter(Q(course_name__icontains=q) | Q(course_type__course_type__exact=q)).distinct('course_name')
                
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
def list_popular_university(request):
    course=request.query_params.get('course')
    country=request.query_params.get('country')
    specialization=request.query_params.get('specialization')
    if specialization:
        university = University.objects.filter(country__in=country,course__course_name=course,specialization__specialization_name=specialization,is_deleted=False).distinct('university_name')
        if university.exists():
            serialized_data=PopularUniversitySerializer(university,
                             context={
                                 "request":request,
                             },
                             many=True,).data
            response_data={
                "StatusCode":6000,
                "data":
                    {
                        "university":serialized_data
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
        
    elif (university:=University.objects.filter(country__in=country,course__course_name=course,is_deleted=False)).exists():
            serialized_data=PopularUniversitySerializer(university,
                             context={
                                 "request":request,
                             },
                             many=True,).data
            response_data={
                "StatusCode":6000,
                "data":
                    {
                        "university":serialized_data
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
    # else:
    #      response_data={
    #             "StatusCode":6001,
    #             "data":{
    #                 "title":"Failed",
    #                 "Message":"Not Found"
    #             }
    #         }

    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def count_university(request):
    coursetype = request.data.get('coursetype')  
    coursename = request.data.get('coursename')  
    if (course_type:= CourseType.objects.get(id=coursetype, is_deleted=False)):
        if (course := Course.objects.filter(course_name=coursename, university__coursetype=course_type, is_deleted=False)).exists():
            university_count = course.count()
            response_data = {
            "StatusCode": 6000,
            "data": university_count
        }
        else:
            response_data = {
            "StatusCode": 6001,
            "data":[]
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":[]
        }

    return Response({'app_data': response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def compare_university(request):
    course=request.GET.get('course')
    universities=request.GET.getlist('university')
    if (university:=University.objects.filter(id__in=universities,is_deleted=False)).exists():
        serialized_data=CompareUniversitySerializer(university,
                                             context={
                                                 "course":course,
                                                 'request':request,
                                             },many=True,).data
        response_data={
            "StatusCode":6000,
            "data":serialized_data
        }
    else:
        response_data={
            "StatusCode":6001,
            "data":[]
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_single_university_details(request,pk):
    course=request.GET.get('course')
    if (university:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        serialized_data=SingleUniversityDetailsSerializer(university,
                                             context={
                                                 "course":course,
                                                 "request":request,
                                             },many=True,).data
    
        response_data={
            "StatusCode":6000,
            "data": 
            {
                "university":serialized_data, 

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
def list_single_university_fee_details(request,pk):
    coursetype=request.data.get('coursetype')
    course_id=request.data.get('course_id')
    if (course:=Course.objects.filter(university=pk,university__coursetype=coursetype,id=course_id,is_deleted=False)).exists():
           fees_fata=CourseSerializer(course,
                                   context={
                                                 "request":request,
                                             },many=True,).data
           response_data={
            "StatusCode":6000,
            "data":
            {
                "fees_data":fees_fata
            
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
def add_university_option(request,pk):
    option=request.data.get('option')
    if (u:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        university_id=u.latest('id')
        opt_obj=option
        for i in opt_obj:
            options=Options.objects.get(id=i)
            university_obj=university_id.options.add(options)
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

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_university_accreditation(request,pk):
    approved_by=request.data.get('approved_by')
    if (u:=University.objects.filter(pk=pk,is_deleted=False)).exists():
        university_id=u.latest('id')
        acc_obj=approved_by
        for i in acc_obj:
            accreditations=Accreditation.objects.get(id=i)
            university_obj=university_id.approved_by.add(accreditations)
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

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_university(request):
    universities = University.objects.all()
    if universities.exists():
        universities.update(is_deleted=True)
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
@group_required(['ezgrad_admin'])
def add_facility_type(request):
    serialized_data=AddFacilityTypeSerializer(data=request.data)
    if serialized_data.is_valid():
        facility=request.data['facility']
        f=FacilityType.objects.create(facility=facility)
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

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_facility_type(request):
    if (facility:=FacilityType.objects.filter(is_deleted=False)).exists():
        serialized_data=FacilityTypeSerializer(facility,
                                               context={
                                                   'request':request,
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
@group_required(['ezgrad_admin'])
def view_single_facility_type(request,pk):
    if (facility:=FacilityType.objects.filter(pk=pk,is_deleted=False)).exists():
        serialized_data=FacilityTypeSerializer(facility,
                                               context={
                                                   'request':request,
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


@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_facility_type(request,pk):
    if (facilities:=FacilityType.objects.filter(pk=pk,is_deleted=False)).exists():
        f=facilities.latest('id')
        facility=request.data.get('facility')
        if facility:
            f.facility=facility
        f.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Edited Successfully"
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
def delete_facility_type(request,pk):
    if (facilities:=FacilityType.objects.filter(pk=pk,is_deleted=False)).exists():
        f=facilities.latest('id')
        f.is_deleted=True
        f.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"deleted Successfully"
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
def add_facilities(request):
    serialized_data=AddFacilitiesSerializer(data=request.data)
    if serialized_data.is_valid():
        name=request.data['name']
        image=request.data.get('image')
        distance=request.data['distance']
        fee=request.data['fee']
        university=request.data.get('university')
        facility=request.data.get('facility')
        if (u:=University.objects.filter(pk=university,is_deleted=False)).exists():
            university_id=u.latest('id')
            if (f:=FacilityType.objects.filter(pk=facility,is_deleted=False)).exists():
                facilities=f.latest('id')
                facility_data=Facilities.objects.create(university=university_id,facility=facilities,
                                                        name=name,
                                                        image=image,
                                                        distance=distance,
                                                        fee=fee)
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
                        "Message":"facility Not Found"
                    }
                }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"university Not Found"
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

@api_view(['GET'])  
@group_required(['ezgrad_admin'])
def view_facilities(request,pk):
    if (facilities:=Facilities.objects.filter(facility=pk,is_deleted=False)).exists():
        serialized_data=FacilitiesSerializer(facilities,
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
@group_required(['ezgrad_admin'])
def view_university_facilities(request):
    university=request.GET.get('university')
    facility=request.GET.get('facility')
    if university and facility:
        if (facility:=FacilityType.objects.filter(id=facility,is_deleted=False)).exists():
            f=facility.latest('id')
            if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
                u=u.latest('id')
                if (facilities:=Facilities.objects.filter(university=u,facility=f,is_deleted=False)).exists():
                    serialized_data=FacilitiesSerializer(facilities,
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
                    
    elif facility:
        if (facility:=FacilityType.objects.filter(id=facility,is_deleted=False)).exists():
            f=facility.latest('id')
            if (facilities:=Facilities.objects.filter(facility=f,is_deleted=False)).exists():
                serialized_data=FacilitiesSerializer(facilities,
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
        else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Not Found"
                    }
                }
    elif university:
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            u=u.latest('id')
            if (facilities:=Facilities.objects.filter(university=u,is_deleted=False)).exists():
                serialized_data=FacilitiesSerializer(facilities,
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
    else:
            if (facilities:=Facilities.objects.filter(is_deleted=False)).exists():
                serialized_data=FacilitiesSerializer(facilities,
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
@group_required(['ezgrad_admin'])
def view_single_facilities(request,id):
    if (facilities:=Facilities.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=FacilitiesSerializer(facilities,
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


@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_facilities(request,id):
    name=request.data.get('name')
    image=request.data.get('image')
    distance=request.data.get('distance')
    fee=request.data.get('fee')
    if (f:=Facilities.objects.filter(id=id,is_deleted=False)).exists():
        facility=f.latest('id')
        if name:
            facility.name=name
        if image:
            facility.image=image
        if distance:
            facility.distance=distance
        if fee:
            facility.fee=fee
        facility.save()
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
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_facilities(request,id):
    if (f:=Facilities.objects.filter(id=id,is_deleted=False)).exists():
        facility=f.latest('id')
        facility.is_deleted=True
        facility.save()
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_facilities(request,pk):
    if (facility:=FacilityType.objects.filter(pk=pk,is_deleted=False)).exists():
        f=facility.latest('id')
        university=request.query_params.get('university')
        if (facilities:=Facilities.objects.filter(university=university,facility=f,is_deleted=False)).exists():
            serialized_data=FacilitiesSerializer(facilities,
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
    else:
        response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Not Found"
                }
            }
    return Response({'app_data':response_data})



# @api_view(['GET'])
# def filter_university(request):
#         student=request.data.get('student')
#         options=request.data.getlist('option')
#         for i in options:
#             if (student_profile := StudentProfile.objects.filter(id=student)) is not None:
#                 s=student_profile.latest('id')
#                 record = RecordAnswer.objects.filter(userid=s)
#                 if record.exists():     
#                     latest_record = record.latest('id')

            
#                     universities = University.objects.filter(options=latest_record.option)

            
#                     serialized_data = UniversitySerializer(universities, context={"request": request},many=True,).data

#                     response_data={
#                     "StatusCode":6000,
#                     "data":serialized_data
#                 }
#             else:
#                 response_data={
#                     "StatusCode":6001,
#                     "data":{
#                         "title":"Failed",
#                         "Message":"Not Found"
#                     }
#                 }
#         else:
#             response_data={
#                 "StatusCode":6001,
#                     "data":{
#                         "title":"Failed",
#                         "Message":"Not Found"
#                     }
#             }
#         return Response({'app_data':response_data})
    


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_facts(request):
    serialized_data=AddFactSerializer(data=request.data)
    if serialized_data.is_valid():
        facts=request.data['facts']
        university=request.data.get('university')
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            u=u.latest('id')
            fact=Facts.objects.create(university=u,
                                      facts=facts)
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
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})
    

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_facts(request):
    if (fact:=Facts.objects.filter(is_deleted=False)).exists():
        serialized_data=FactSerializer(fact,
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_facts(request,id):
    if (fact:=Facts.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=FactSerializer(fact,
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
    
@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_facts(request,id):
    facts=request.data.get('facts')
    university=request.data.get('university')
    if (fact:=Facts.objects.filter(id=id,is_deleted=False)).exists():
        fact=fact.latest('id')
        if facts:
            fact.facts=facts
        if university:
            u=University.objects.get(id=university)
            fact.university=u
        fact.save()
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
    return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_facts(request,id):
    if (fact:=Facts.objects.filter(id=id,is_deleted=False)).exists():
        fact=fact.latest('id')
        fact.is_deleted=True
        fact.save()
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

class UniversitySelection(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(group_required(['ezgrad_admin']))
    def get(self, request):
        try:
            university_instance = University.objects.filter(is_deleted=False).values('university_name', 'id')
            University_list = list(university_instance)
            response_data = {
                "StatusCode": 6000,
                "data": University_list
            }
        except University.DoesNotExist:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": "Univercity not found"
                }
            }
        except Exception as e:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": str(e)
                }
            }

        return Response({'app_data': response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_university_image(request):
    serialized_data=AddUniversityImageSerializer(data=request.data)
    if serialized_data.is_valid():
        image=request.data['image']
        university=request.data.get('university')
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            u=u.latest('id')
            image_data=UniversityImages.objects.create(university=u,
                                                        image=image)
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
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})
    


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_university_image(request):
    if (u_image:=UniversityImages.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversityImageSerializer(u_image,
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_university_image(request,id):
    if (u_image:=UniversityImages.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=UniversityImageSerializer(u_image,
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
   
@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_university_image(request,id):
    image=request.data.get('image')
    university=request.data.get('university')
    if (u_image:=UniversityImages.objects.filter(id=id,is_deleted=False)).exists():
        u_image=u_image.latest('id')
        if image:
            u_image.image=image
        if university:
            u=University.objects.get(id=university,is_deleted=False)
            u_image.university=u
        u_image.save()
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
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_university_image(request,id):
    if (u_image:=UniversityImages.objects.filter(id=id,is_deleted=False)).exists():
        u_image=u_image.latest('id')
        u_image.is_deleted=True
        u_image.save()
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
def add_accreditation(request):
    serialized_data=AddAccreditationSerializer(data=request.data)
    if serialized_data.is_valid():
        approved_by=request.data['approved_by']
        name=request.data['name']
        logo=request.data['logo']
        accreditation=Accreditation.objects.create(approved_by=approved_by,
                                                   name=name,
                                                   logo=logo)
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_accreditation(request,id):
    if (a:=Accreditation.objects.filter(id=id,is_deleted=False)).exists():
        acc=a.latest('id')
        approved_by=request.data.get('approved_by')
        name=request.data.get('name')
        logo=request.data.get('logo')
        if approved_by:
            acc.approved_by=approved_by
        if name:
            acc.name=name
        if logo:
            acc.logo=logo
        acc.save()
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
    return Response({'app_data':response_data})
        
@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_accreditation(request):
    if (acc:=Accreditation.objects.filter(is_deleted=False)).exists():
        serialized_data=AccreditationSerializer(acc,
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
@group_required(['ezgrad_admin'])
def view_single_accreditation(request,id):
    if (acc:=Accreditation.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=AccreditationSerializer(acc,
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


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_accreditation(request,id):
    if (acc:=Accreditation.objects.filter(id=id,is_deleted=False)).exists():
        a=acc.latest('id')
        a.is_deleted=True
        a.save()
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


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_accreditation(request):
    accreditation = Accreditation.objects.all()
    if accreditation.exists():
        accreditation.update(is_deleted=True)
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
@group_required(['ezgrad_admin'])
def add_accreditation_points(request):
    serialized_data=AddAccreditationPointsSerializer(data=request.data)
    if serialized_data.is_valid():
        points=request.data['points']
        accreditation=request.data.get('accreditation')
        if (a:=Accreditation.objects.filter(id=accreditation,is_deleted=False)).exists():
            approval=a.latest('id')
            accreditation_points=AccreditationPoints.objects.create(approval=approval,
                                                                    points=points)
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
                    "Message":"Accreditation Not Found"
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

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_accreditation_points(request,id):
    if (a:=AccreditationPoints.objects.filter(approval=id,is_deleted=False)).exists():
        serialized_data=AccreditationPointSerializer(a,
                                                     context={
                                                         'request':request,
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_accreditation_points(request,id):
    if (a:=AccreditationPoints.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=AccreditationPointSerializer(a,
                                                     context={
                                                         'request':request,
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


@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_accreditation_points(request,id):
    if (a:=AccreditationPoints.objects.filter(id=id,is_deleted=False)).exists():
        accreditation=a.latest('id')
        points=request.data.get('points')
        if points:
            accreditation.points=points
        accreditation.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Updated SUccessfully"
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
def delete_accreditation_points(request,id):
    if (a:=AccreditationPoints.objects.filter(id=id,is_deleted=False)).exists():
        a=a.latest('id')
        a.is_deleted=True
        a.save()
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

@api_view(['GET'])
@permission_classes([AllowAny])
def fact_list(request):
    university=request.data.get('university')
    if (facts:=Facts.objects.filter(university=university,is_deleted=False)).exists():
        serialized_data=FactSerializer(facts,
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



@api_view(['GET'])
@permission_classes([AllowAny])
def list_university_logo(request):
    if (university:=University.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversitySerializer(university,
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


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_general_course(request):
    serialized_data=AddCourseSerializer(data=request.data)
    if serialized_data.is_valid():
        course_name=request.data['course_name']
        duration=request.data['duration']
        duration_description=request.data.get('duration_description')
        course_image=request.data['course_image']
        course_details=request.data.get('course_details')
        eligibility=request.data['eligibility']
        eligibility_description=request.data.get('eligibility_description')
        admission_procedure=request.data.get('admission_procedure')
        semester_fee=request.data['semester_fee']
        fees_description=request.data.get('fees_description')
        if Course.objects.filter(course_name=course_name,type="general").exists():
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Already Exist Course General details"
                }
            }
        else:
            course=Course.objects.create(course_name=course_name,
                                        duration=duration,
                                        duration_description=duration_description,
                                        course_image=course_image,
                                        course_details=course_details,
                                        eligibility=eligibility,
                                        eligibility_description=eligibility_description,
                                        admission_procedure=admission_procedure,
                                        semester_fee=semester_fee,
                                        fees_description=fees_description,
                                        type="general",
                                        )
            response_data={
                        "StatusCode":6000,
                        "data":{
                            "title":"Success",
                            "Message":"Successfully added"
                        }
                    }
    else:
            response_data={
                "StatusCode":6001,
                "data":
                {
                    "title":"Failed",
                    "Message":generate_serializer_errors(serialized_data._errors)
                }
            }
    return Response({'app_data':response_data})
            

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_course(request):
    serialized_data=AddCourseSerializer(data=request.data)
    if serialized_data.is_valid():
        university=request.data.get('university')
        course_type=request.data.get('coursetype')
        course_name=request.data['course_name']
        icon=request.data['icon']
        duration=request.data['duration']
        duration_description=request.data.get('duration_description')
        course_image=request.data['course_image']
        course_details=request.data.get('course_details')
        video=request.data.get('video')
        audio=request.data.get('audio')
        eligibility=request.data['eligibility']
        eligibility_description=request.data.get('eligibility_description')
        admission_procedure=request.data.get('admission_procedure')
        semester_fee=request.data.get('semester_fee')
        year_fee=request.data.get('year_fee')
        fees_description=request.data.get('fees_description')
        syllabus=request.data['syllabus']
        slug=request.data['slug']
        renamed_slug=slug.replace(' ','-')
        type=request.data.get('type')
  
        # full_fee=int(duration)*int(year_fee)
        if duration is not None :
            full_fee = int(duration) * int(year_fee)
        else:
            full_fee = None
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
                u=u.latest('id')
        
                if (coursetype:=CourseType.objects.filter(id=course_type)).exists():
                    course_types=coursetype.latest('id')
                    if (p:=Course.objects.filter(is_deleted=False,slug=renamed_slug)).exists():
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Slug Already Exist"
                            }
                        }
                    else:
                        course=Course.objects.create(university=u,
                                                    course_type=course_types,
                                                    course_name=course_name,
                                                    icon=icon,
                                                    duration=duration,
                                                    duration_description=duration_description,
                                                    course_image=course_image,
                                                    course_details=course_details,
                                                    video=video,
                                                    audio=audio,
                                                    eligibility=eligibility,
                                                    eligibility_description=eligibility_description,
                                                    admission_procedure=admission_procedure,
                                                    semester_fee=semester_fee,
                                                    year_fee=year_fee,
                                                    full_fee=full_fee,
                                                    fees_description=fees_description,
                                                    syllabus=syllabus,
                                                    slug=renamed_slug,
                                                    type=type)
                        response_data={
                            "StatusCode":6000,
                            "data":{
                                "title":"Success",
                                "Message":"Successfully added"
                            }
                        }
                else:
                    course=Course.objects.create(university=u,
                                                course_name=course_name,
                                                icon=icon,
                                                duration=duration,
                                                duration_description=duration_description,
                                                course_image=course_image,
                                                course_details=course_details,
                                                video=video,
                                                audio=audio,
                                                eligibility=eligibility,
                                                eligibility_description=eligibility_description,
                                                admission_procedure=admission_procedure,
                                                semester_fee=semester_fee,
                                                full_fee=full_fee,
                                                fees_description=fees_description,
                                                syllabus=syllabus,
                                                slug=renamed_slug,
                                                type=type)
                    response_data={
                        "data":{
                            "title":"Success",
                            "Message":"Added Successfully"
                        }
                    }
           
        else:
            response_data={
                "data":{
                    "title":"Failed",
                    "Message":"University Not Found"
                }
            }
    else:
            response_data={
                "StatusCode":6001,
                "data":
                {
                    "title":"Failed",
                    "Message":generate_serializer_errors(serialized_data._errors)
                }
            }
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_course(request):
    if (course:=Course.objects.filter(is_deleted=False)).exists():
        serialized_data=CourseSerializer(course,
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

class CourseSelection(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(group_required(['ezgrad_admin']))
    def get(self, request):
        university = request.query_params.get('university')
        if not university:
            return Response({
                'app_data': {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Failed",
                        "Message": "University parameter is required"
                    }
                }
            }, status=400)
        
        try:
            courses = Course.objects.filter(university=university).values('course_name', 'id')
            course_list = list(courses)
            response_data = {
                "StatusCode": 6000,
                "data": course_list
            }
        except Course.DoesNotExist:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": "Courses not found"
                }
            }
        except Exception as e:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": str(e)
                }
            }

        return Response({'app_data': response_data})

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_course(request,pk):
    if (course:=Course.objects.filter(pk=pk,is_deleted=False)).exists():
        serialized_data=CourseSerializer(course,
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_course(request,pk):
    course_name=request.data.get('course_name')
    icon=request.data.get('icon')
    duration=request.data.get('duration')
    duration_description=request.data.get('duration_description')
    course_image=request.data.get('course_image')
    course_details=request.data.get('course_details')
    video=request.data.get('video')
    audio=request.data.get('audio')
    eligibility=request.data.get('eligibility')
    eligibility_description=request.data.get('eligibility_description')
    admission_procedure=request.data.get('admission_procedure')
    fees=request.data.get('semester_fee')
    fees_description=request.data.get('fees_description')
    syllabus=request.data.get('syllabus')
    slug=request.data.get('slug')
    if (course:=Course.objects.filter(pk=pk,is_deleted=False)).exists():
        course=course.latest('id')
        if course_name:
            course.course_name=course_name
        if icon:
            course.icon=icon
        if duration:
            course.duration=duration
        if duration_description:
            course.duration_description=duration_description
        if course_image:
            course.course_image=course_image
        if course_details:
            course.course_details=course_details
        if video:
            course.video=video
        if audio:
            course.audio=audio
        if eligibility:
            course.eligibility=eligibility
        if eligibility_description:
            course.eligibility_description=eligibility_description
        if admission_procedure:
            course.admission_procedure=admission_procedure
        if fees:
            course.semester_fee=fees
        if fees_description:
            course.fees_description=fees_description
        if syllabus:
            course.syllabus=syllabus
        if slug:
            renamed_slug=slug.replace(' ','-')
            if (p:=Course.objects.filter(is_deleted=False,slug=renamed_slug)).exclude(id=course.id).exists():
                    response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                            "title" : "Failed",
                            "message" : "Slug Already Exist"
                    }
                    }
                    return Response(response_data)
            else:
                course.slug=renamed_slug
        course.save()
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
    return Response({'app_data':response_data})


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_course(request,pk):
    if (course:=Course.objects.filter(pk=pk,is_deleted=False)).exists():
        course=course.latest('id')
        course.is_deleted=True
        course.save()
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


class SpecialisationSelection(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(group_required(['ezgrad_admin']))
    def get(self, request):
        try:
            specialization_instance = Specialization.objects.filter(is_deleted=False).values('specialization_name', 'id')
            specialization_list = list(specialization_instance)
            response_data = {
                "StatusCode": 6000,
                "data": specialization_list
            }
        except Specialization.DoesNotExist:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": "Specializations not found"
                }
            }
        except Exception as e:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Failed",
                    "Message": str(e)
                }
            }

        return Response({'app_data': response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_specialization(request):
    serialized_data=AddSpecializationSerializer(data=request.data)
    if serialized_data.is_valid():
        university=request.data.get('university')
        course=request.data.get('course')
        specialization_name=request.data['specialization_name']
        duration=request.data.get('duration')
        duration_description=request.data.get('duration_description')
        specialization_image=request.data.get('specialization_image')
        specialization_details=request.data.get('specialization_details')
        video=request.data.get('video')
        audio=request.data.get('audio')
        eligibility=request.data.get('eligibility')
        eligibility_description=request.data.get('eligibility_description')
        admission_procedure=request.data.get('admission_procedure')
        semester_fee=request.data.get('semester_fee')
        year_fee=request.data.get('year_fee')
        fees_description=request.data.get('fees_description')
        syllabus=request.data.get('syllabus')
        slug=request.data['slug']
        renamed_slug=slug.replace(' ','-')
        
        if duration is not None :
            full_fee = int(duration) * int(year_fee)
        else:
            full_fee = None
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            u=u.latest('id')
            if (course:=Course.objects.filter(id=course)).exists():
                    course=course.latest('id')
                    if (p:=Specialization.objects.filter(is_deleted=False,slug=renamed_slug)).exists():
                        response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                "title" : "Failed",
                                "message" : "Slug Already Exist"
                            }
                        }
                    else:
                        specialization=Specialization.objects.create(university=u,
                                                    course=course,
                                                    specialization_name=specialization_name,
                                                    duration=duration,
                                                    duration_description=duration_description,
                                                    specialization_image=specialization_image,
                                                    specialization_details=specialization_details,
                                                    video=video,
                                                    audio=audio,
                                                    eligibility=eligibility,
                                                    eligibility_description=eligibility_description,
                                                    admission_procedure=admission_procedure,
                                                    semester_fee=semester_fee,
                                                    year_fee=year_fee,
                                                    full_fee=full_fee,
                                                    fees_description=fees_description,
                                                    syllabus=syllabus,
                                                    slug=renamed_slug)
                        response_data={
                            "StatusCode":6000,
                            "data":{
                                "title":"Success",
                                "Message":"Successfully added"
                            }
                        }
                    
            else:
                response_data={
                    "data":{
                        "title":"Failed",
                        "Message":"Course Not Found"
                    }
                }
        else:
            response_data={
                "data":{
                    "title":"Failed",
                    "Message":"University Not Found"
                }
            }
    else:
            response_data={
                "StatusCode":6001,
                "data":
                {
                    "title":"Failed",
                    "Message":generate_serializer_errors(serialized_data._errors)
                }
            }
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_specialization(request):
    if (specialization:=Specialization.objects.filter(is_deleted=False)).exists():
        serialized_data=SpecializationSerializer(specialization,
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_specialization(request,pk):
    if (specialization:=Specialization.objects.filter(pk=pk,is_deleted=False)).exists():
        serialized_data=SpecializationSerializer(specialization,
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

@api_view(['PUT', 'PATCH'])
@group_required(['ezgrad_admin'])
def edit_specialization(request,pk):
        university=request.data.get('university')
        course=request.data.get('course')
        specialization_name=request.data.get('specialization_name')
        duration=request.data.get('duration')
        duration_description=request.data.get('duration_description')
        specialization_image=request.data.get('specialization_image')
        specialization_details=request.data.get('specialization_details')
        video=request.data.get('video')
        audio=request.data.get('audio')
        eligibility=request.data.get('eligibility')
        eligibility_description=request.data.get('eligibility_description')
        admission_procedure=request.data.get('admission_procedure')
        fees=request.data.get('semester_fee')
        fees_description=request.data.get('fees_description')
        syllabus=request.data.get('syllabus')
        slug=request.data.get('slug')
        if (course_specialization:=Specialization.objects.filter(pk=pk,is_deleted=False)).exists():
            c=course_specialization.latest('id')
            if university:
                c.university=University.objects.filter(id=university).first()
            if course:
                c.course=Course.objects.filter(id=course).first()
            if specialization_name:
                c.specialization_name=specialization_name
            if duration:
                c.duration=duration
            if duration_description:
                c.duration_description=duration_description
            if specialization_image:
                c.specialization_image=specialization_image
            if specialization_details:
                c.specialization_details=specialization_details
            if video:
                c.video=video
            if audio:
                c.audio=audio
            if eligibility:
                c.eligibility=eligibility
            if eligibility_description:
                c.eligibility_description=eligibility_description
            if admission_procedure:
                c.admission_procedure=admission_procedure
            if fees:
                c.semester_fee=fees
            if fees_description:
                c.fees_description=fees_description
            if syllabus:
                c.syllabus=syllabus
            if slug:
                renamed_slug=slug.replace(' ','-')
                if (p:=Specialization.objects.filter(is_deleted=False,slug=renamed_slug)).exclude(id=c.id).exists():
                        response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                                "title" : "Failed",
                                "message" : "Slug Already Exist"
                                }
                            }
                        return Response(response_data)
                else:
                    c.slug=renamed_slug
            c.save()
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
        return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_specialization(request,pk):
    if (specialization:=Specialization.objects.filter(pk=pk,is_deleted=False)).exists():
        s=specialization.latest('id')
        s.is_deleted=True
        s.save()
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



@api_view(['GET'])
@permission_classes([AllowAny])
def list_specialization(request):
    course=request.GET.get('course')
    if (specialization:=Specialization.objects.filter(course__course_name=course,is_deleted=False)).exists():
        if (distinct_specialization := specialization.distinct('specialization_name')):
            # s=specialization.latest('id')
            # university_count=Specialization.objects.filter(course=s.course,is_deleted=False).values('university').distinct().count()
            serialized_data=SpecializationSerializer(distinct_specialization,
                                                        context={
                                                            "request":request,
                                                        },
                                                        many=True,).data
            response_data={
                "StatusCode":6000,
                "data":{
                    "specialization": serialized_data,
                    # "count":university_count,
                
                
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
def list_specialization_studentform(request):
    course=request.query_params.get('course')
    specialization=request.query_params.get('specialization')
    if specialization and course:
        university_count=Specialization.objects.filter(course=course,is_deleted=False).values('university').distinct().count()
        s=Specialization.objects.filter(pk=specialization,course=course,is_deleted=False)
        if s:
            serialized_data=SpecializationSerializer(s,
                                                     context={
                                                         "request":request,
                                                     },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data,
                "count":university_count
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Specialization Not Found"
                }
            }
    
    else:
         response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"Course Not Found"
                }
            }
        
    return Response({'app_data':response_data})

@api_view(['GET'])
@permission_classes([AllowAny])
def list_courses(request):
    service = request.query_params.get('service')
    coursetype = request.query_params.get('coursetype')
    response_data = {}
    if coursetype:
        if (coursetypes := CourseType.objects.filter(id=coursetype, service=service, is_deleted=False)).exists():
            if service:
                if (course := Course.objects.filter(university__service_id=service, course_type=coursetype, is_deleted=False)).exists():
                    if (distinct_course := course.distinct('course_name')):
                        serialized_data = CourseviewSerializer(distinct_course,
                                                                context={
                                                                    "request": request,
                                                                },
                                                                many=True, ).data
                        response_data = {
                            "StatusCode": 6000,
                            "data": serialized_data
                        }

                    else:
                        response_data = {
                            "StatusCode": 6001,
                            "data": []
                        }
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "data": []
                    }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": []
                }
    elif (courses := Course.objects.filter(university__service_id=service,is_deleted=False)).exists():
        if (distinct_courses := courses.distinct('course_name')):
            c_data = CourseviewSerializer(distinct_courses,
                                            context={
                                                "request": request,
                                            }, many=True).data
            response_data = {
                "StatusCode": 6000,
                "data": c_data
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }

    elif (courses := Course.objects.filter(is_deleted=False)).exists():
        if (distinct_courses := courses.distinct('course_name')):
            course_data = CourseviewSerializer(distinct_courses,
                                               context={
                                                   "request": request,
                                               }, many=True).data
            response_data = {
                "StatusCode": 6000,
                "data": course_data
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": []
        }
    
    return Response({'app_data': response_data})




@api_view(['GET'])
@permission_classes([AllowAny])
def list_courses_suggest(request):
    service = request.query_params.get('service')
    if service:
        if (courses := Course.objects.filter(university__service_id=service,is_deleted=False)).exists():
            if (distinct_courses := courses.distinct('course_name')):
                c_data = CourseviewSerializer(distinct_courses,
                                                context={
                                                    "request": request,
                                                }, many=True).data
                response_data = {
                    "StatusCode": 6000,
                    "data": c_data
                }
            else:
                response_data={
                    "StatusCode":6001,
                    "data":[]
                }

        else:
            response_data = {
                "StatusCode": 6001,
                "data": []
            }
    else:
            response_data = {
                "StatusCode": 6001,
                "data": []
            }
    
    return Response({'app_data': response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_course_country(request):
    service=request.GET.get('service')
    coursetype=request.GET.get('coursetype')
    coursename=request.GET.get('coursename')
    if (coursetypes:=CourseType.objects.filter(id=coursetype,service=service,is_deleted=False)).exists():
        coursetypes=coursetypes.latest('id')
        if (course:=Course.objects.filter(university__service_id=service,course_type=coursetypes,course_name=coursename,is_deleted=False)).exists():
            serialized_data=CourseCountrySerializer(course,
                                                    context={
                                                        'request':request,
                                                    },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data
            }
        else:
            response_data={
            "StatusCode":6001,
            "data":[]
        }
    else:
        if (course:=Course.objects.filter(university__service_id=service,course_name=coursename,is_deleted=False)).exists():
            serialized_data=CourseCountrySerializer(course,
                                                    context={
                                                        'request':request,
                                                    },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_regular_states(request):
    service=request.GET.get('service')
    coursetype=request.GET.get('coursetype')
    coursename=request.GET.get('coursename')
    if (coursetypes:=CourseType.objects.filter(id=coursetype,service=service,is_deleted=False)).exists():
        coursetypes=coursetypes.latest('id')
        if (course:=Course.objects.filter(university__service_id=service,course_type=coursetypes,course_name=coursename,is_deleted=False)).exists():
            serialized_data=CourseStateSerializer(course,
                                                    context={
                                                        'request':request,
                                                    },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data
            }
        else:
            response_data={
            "StatusCode":6001,
            "data":[]
        }
    else:
        if (course:=Course.objects.filter(university__service_id=service,course_name=coursename,is_deleted=False)).exists():
            serialized_data=CourseCountrySerializer(course,
                                                    context={
                                                        'request':request,
                                                    },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }
    return Response({'app_data':response_data})



@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def bulk_remove_specialization(request):
    specialization = Specialization.objects.all()
    if specialization.exists():
        specialization.update(is_deleted=True)
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
@group_required(['ezgrad_admin'])
def add_country(request):
    serialized_data=AddCountrySerializer(data=request.data)
    if serialized_data.is_valid():
        country=request.data['country']
        flag=request.data['flag']
        c=Country.objects.create(country=country,flag=flag)
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Added Successfully",
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_country(request):
    if (country:=Country.objects.filter(is_deleted=False)).exists():
        serialized_data=CountrySerializer(country,
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_country(request,id):
    if (country:=Country.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=CountrySerializer(country,
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



@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_country(request,id):
    country=request.data.get('country')
    flag=request.data.get('flag')
    if (c:=Country.objects.filter(id=id,is_deleted=False)).exists():
        c=c.latest('id')
        if country:
            c.country=country
        if flag:
            c.flag=flag
        c.save()
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
    return Response({'app_data':response_data})




@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_country(request,id):
    if (country:=Country.objects.filter(id=id,is_deleted=False)).exists():
        c=country.latest('id')
        c.is_deleted=True
        c.save()
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_country(request):
    coursetype = request.data.get('coursetype')  
    coursename = request.data.get('coursename')  
    if (course_type:= CourseType.objects.get(id=coursetype, is_deleted=False)):
        if (course := Course.objects.filter(course_name=coursename, university__coursetype=course_type, is_deleted=False)).exists():
            serialized_data=CourseviewSerializer(course,
                                                 context={
                                                     'request':request,
                                                 },many=True,).data
            response_data={
                "StatusCode":6000,
                "data":serialized_data
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }
    else:
        response_data={
            "StatusCode":6001,
            "data":[]
        }
    return Response({'app_data':response_data})


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_faq(request):
    serialized_data=AddFaqSerializer(data=request.data)
    if serialized_data.is_valid():
        course=request.data.get('course')
        specialization=request.data.get('specialization')
        if course:
            if (c:=Course.objects.filter(id=course,is_deleted=False)).exists():
                course_id=c.latest('id')
                faq_question=request.data['faq_question']
                faq_answer=request.data['faq_answer']
                faq=Faq.objects.create(course=course_id,faq_question=faq_question,
                                    faq_answer=faq_answer)
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
                        "Message":"Course Not Found"
                    }

                }
        elif specialization:
            if (c:=Specialization.objects.filter(id=specialization,is_deleted=False)).exists():
                s=c.latest('id')
                faq_question=request.data['faq_question']
                faq_answer=request.data['faq_answer']
                faq=Faq.objects.create(specialization=s,faq_question=faq_question,
                                    faq_answer=faq_answer)
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
                        "Message":"Specialization Not Found"
                    }

                }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":" Not Found"
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_faq(request):
    if (faq:=Faq.objects.filter(is_deleted=False)).exists():
        serialized_data=FaqSerializer(faq,
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_faq(request,id):
    if (faq:=Faq.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=FaqSerializer(faq,
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_faq(request,id):
        faq_question=request.data.get('faq_question')
        faq_answer=request.data.get('faq_answer')
        if (faq:=Faq.objects.filter(id=id,is_deleted=False)).exists():
            f=faq.latest('id')
            if faq_question:
                f.faq_question=faq_question
            if faq_answer:
                f.faq_answer=faq_answer
            f.save()
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
        return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_faq(request,id):
    if (faq:=Faq.objects.filter(id=id,is_deleted=False)).exists():
        f=faq.latest('id')
        f.is_deleted=True
        f.save()
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

@api_view(['GET'])
@permission_classes([AllowAny])
def list_faq(request,pk):
    if (faq:=Faq.objects.filter(course=pk,is_deleted=False)).exists():
        serialized_data=FaqSerializer(faq,
                         context={
                             "request":request,
                         },
                         many=True,).data
        response_data={
            "StatusCode":6000,
            "data":serialized_data
        }
    elif (faq:=Faq.objects.filter(specialization=pk,is_deleted=False)).exists():
        serialized_data=FaqSerializer(faq,
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


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_currency(request):
    serialized_data=AddcurrencySerializer(data=request.data)
    if serialized_data.is_valid():
        symbol=request.data['symbol']
        symbol_name=request.data['symbol_name']
        currency=CurrencySymbol.objects.create(symbol=symbol,
                                               symbol_name=symbol_name)
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Added SUccessfully"
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

@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_currency(request):
    if (c:=CurrencySymbol.objects.filter(is_deleted=False)).exists():
        serialized_data=CurrencySerializer(c,
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_currency(request,id):
    if (c:=CurrencySymbol.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=CurrencySerializer(c,
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_currency(request,id):
    symbol=request.data.get('symbol')
    symbol_name=request.data.get('symbol_name')
    if (c:=CurrencySymbol.objects.filter(id=id,is_deleted=False)).exists():
        currency=c.latest('id')
        if symbol:
            currency.symbol=symbol
        if symbol_name:
            currency.symbol_name=symbol_name
        currency.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Updated Succesfully"
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
def list_currency(request):
    if (c:=CurrencySymbol.objects.filter(is_deleted=False)).exists():
        c=c.order_by("order_id")
        serialized_data=CurrencySerializer(c,
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



@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_currency(request,id):
    if (currency:=CurrencySymbol.objects.filter(id=id,is_deleted=False)).exists():
        f=currency.latest('id')
        f.is_deleted=True
        f.save()
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

@api_view(['GET'])
@permission_classes([AllowAny])
def convert_currency(request, id):
    currency_symbol = CurrencySymbol.objects.filter(id=id).first()

    if currency_symbol:
        amount = request.query_params.get('amount')
        source_currency = currency_symbol.source_currency
        target_currency = request.query_params.get('target_currency')
        course=request.GET.get('course')
        year=request.GET.get('year')
        if not all([amount, source_currency, target_currency]):
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

        conversion_api_url = f'https://api.exchangerate-api.com/v4/latest/{source_currency}'
        response = requests.get(conversion_api_url)

        if response.status_code == 200:
            data = response.json()
            exchange_rate = data['rates'].get(target_currency)

            if exchange_rate is not None:
               
                converted_amount = float(amount) * exchange_rate 
                rounded_amount = round(converted_amount, 2)
                currency_symbol.converted_amount = rounded_amount
                currency_symbol.save()
                currency = CurrencySymbol.objects.get(symbol_name=target_currency)
                if currency:
                    target_currency=currency.symbol
                else:
                    target_currency= ""

                if (c:=Course.objects.filter(id=course,year_fee__isnull=False)).exists():
                    cc=c.latest('id')
                    convert_sem_fee=(float(amount )/ float(2)) * exchange_rate
                    y=float(''.join(filter(str.isdigit, year)))
                    convert_full_fee=(float(amount) * float(y)) * exchange_rate
                    cc.converted_year_fee=rounded_amount
                    cc.converted_sem_fee=round(convert_sem_fee)
                    cc.converted_full_fee=round(convert_full_fee)
                    cc.save()
                else:
                    response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Failed",
                        "Message": "Course Not Found"
                    }
                }

                

                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        'converted_amount': rounded_amount,
                        'currency_symbol':target_currency,
                    }
                }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data": {
                        "title": "Failed",
                        "Message": "Conversion not Done"
                    }
                }

            return Response({'app_data': response_data}, status=status.HTTP_200_OK)

    return Response({'error': 'Failed to fetch exchange rate'}, status=response.status_code)




@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_university_banner(request):
    serialized_data=AddUniversityBannerSerializer(data=request.data)
    if serialized_data.is_valid():
        banner=request.data['banner']
        banner_url=request.data.get('banner_url')
        banner=UniversityBanner.objects.create(banner=banner,
                                               banner_url=banner_url)
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_university_banner(request):
    if (banner:=UniversityBanner.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversityBannerSerializer(banner,
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
@group_required(['ezgrad_admin'])
def view_single_university_banner(request,id):
    if (banner:=UniversityBanner.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=UniversityBannerSerializer(banner,
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_university_banner(request,id):
    if (university_banner:=UniversityBanner.objects.filter(id=id,is_deleted=False)).exists():
        banners=university_banner.latest('id')
        banner=request.data.get('banner')
        banner_url=request.data.get('banner_url')
        if banner:
            banners.banner=banner
        if banner_url:
            banners.banner_url=banner_url
        banners.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Edited Successfully"
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
def delete_university_banner(request,id):
    if (banners:=UniversityBanner.objects.filter(id=id,is_deleted=False)).exists():
        banner=banners.latest('id')
        banner.is_deleted=True
        banner.save()
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

@api_view(['GET'])
@permission_classes([AllowAny])
def list_university_banner(request):
    if (banners:=UniversityBanner.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversityBannerSerializer(banners,
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

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_placement_partner(request):
    serialized_data=AddplacementpartnerSerializer(data=request.data)
    if serialized_data.is_valid():
        university=request.data.get('university')
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            university_id=u.latest('id')
            placement_partner_name=request.data['placement_partner_name']
            placement_partner_logo=request.data['placement_partner_logo']
            placement=PlacementPartners.objects.create(university=university_id,
                                                    placement_partner_name=placement_partner_name,
                                                    placement_partner_logo=placement_partner_logo)
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
                    "Message":"University Not Found"
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

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_placement_partner(request,id):
    placement_partner_name=request.data.get('placement_partner_name')
    placement_partner_logo=request.data.get('placement_partner_logo')
    if (placement_data:=PlacementPartners.objects.filter(id=id,is_deleted=False)).exists():
        placement=placement_data.latest('id')
        if placement_partner_name:
            placement.placement_partner_name=placement_partner_name
        if placement_partner_logo:
            placement.placement_partner_logo=placement_partner_logo
        placement.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Mesage":"Updated Successfully"
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
def delete_placement_partner(request,id):
    if (placement_data:=PlacementPartners.objects.filter(id=id,is_deleted=False)).exists():
        placement=placement_data.latest('id')
        placement.is_deleted=True
        placement.save()
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_placement_partner(request):
    if (placement:=PlacementPartners.objects.filter(is_deleted=False)).exists():
        serialized_data=PlacementPartnerSerializer(placement,
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
@group_required(['ezgrad_admin'])
def view_single_placement_partner(request,id):
    if (placement:=PlacementPartners.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=PlacementPartnerSerializer(placement,
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
def list_placement_partner(request,pk):
    if (placement:=PlacementPartners.objects.filter(university=pk,is_deleted=False)).exists():
        serialized_data=PlacementPartnerSerializer(placement,
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
# @group_required(['ezgrad_admin'])
@permission_classes([AllowAny])
def search_university(request):
    try:
        q =  request.GET.get('q')
        if (university := University.objects.filter(is_deleted=False)).exists():

            if q:
                university = University.objects.filter(Q(university_name__icontains=q))

            serialized_data = UniversitySerializer(
                university,
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
                    "Message" : "University Not Found"
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
def search_courses(request):
    try:
        q =  request.GET.get('q')
        if (course := Course.objects.filter(is_deleted=False)).exists():

            if q:
                course = course.filter(Q(course_name__icontains=q) | Q(duration__icontains=q) | Q(year_fee__icontains=q | Q(eligibility_icontains=q)))
                
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



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_university_document(request):
    serialized_data=AddUniversityDocumentSerializer(data=request.data)
    if serialized_data.is_valid():
        document_name=request.data['document_name']
        document=request.data['document']
        university=request.data.get('university')
        student=request.data.get('student')
        if (u:=University.objects.filter(id=university,is_deleted=False)).exists():
            university_id=u.latest('id')      
            if (s:=StudentRecord.objects.filter(id=student,is_deleted=False)).exists():
                student_id=s.latest('id')     
                docs=UniversityDocuments.objects.create(university=university_id,
                                                        student=student_id,
                                                        document_name=document_name,
                                                        document=document)
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
                        "Message":"Student Not Found"
                    }
                }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"University Not Found"
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
def edit_university_document(request,id):
    document_name=request.data.get('document_name')
    document=request.data.get('document')
    if (university_data:=UniversityDocuments.objects.filter(id=id,is_deleted=False)).exists():
        doc=university_data.latest('id')
        if document_name:
            doc.document_name=document_name
        if document:
            doc.document=document
        doc.save()
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Mesage":"Updated Successfully"
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
def view_university_document(request):
    if (doc:=UniversityDocuments.objects.filter(is_deleted=False)).exists():
        serialized_data=UniversityDocumentSerializer(doc,
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
@group_required(['ezgrad_admin'])
def view_single_university_document(request,id):
    if (doc:=UniversityDocuments.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=UniversityDocumentSerializer(doc,
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

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_university_document(request,id):
    if (doc:=UniversityDocuments.objects.filter(id=id,is_deleted=False)).exists():
        doc=doc.latest('id')
        doc.is_deleted=True
        doc.save()
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_university_document(request,pk):
    if (doc:=UniversityDocuments.objects.filter(university=pk,is_deleted=False)).exists():
        serialized_data=UniversityDocumentSerializer(doc,
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


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_state(request):
    state_name=request.data.get('state_name')
    country=request.data.get('country')
    if (c:=Country.objects.filter(id=country,is_deleted=False)).exists():
        c=c.latest('id')
        state=States.objects.create(country=c,state_name=state_name)
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Added Successfully"
            }
        }
    else:
        response_data={
            "StatsuCode":6001,
            "data":{
                "title":"Failed",
                "Message":"Country Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def edit_state(request,id):
    if (state:=States.objects.filter(id=id,is_deleted=False)).exists():
        state=state.latest('id')
        state_name=request.data.get('state_name')
        if state_name:
            state.state_name=state_name
        state.save()
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
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_state(request):
    if (state:=States.objects.filter(is_deleted=False)).exists():
        serialized_data=StateSerializer(state,
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_state(request,id):
    if (state:=States.objects.filter(id=id,is_deleted=False)).exists():
        state=state.latest('id')
        serialized_data=StateSerializer(state,
                                        context={
                                            "request":request,
                                        },).data
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
def delete_state(request,id):
    if (state:=States.objects.filter(id=id,is_deleted=False)).exists():
        state=state.latest('id')
        state.is_deleted=True
        state.save()
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


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_states(request,id):
    if (state:=States.objects.filter(country=id,is_deleted=False)).exists():
        serialized_data=StateSerializer(state,
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


@api_view(['GET'])
@permission_classes([AllowAny])
def list_states(request,id):
    if (state:=States.objects.filter(country=id,is_deleted=False)).exists():
        serialized_data=StateSerializer(state,
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


        
@api_view(['GET'])
@permission_classes([AllowAny])
def suggest_university(request):
    list_data = []
    if (questions := Questions.objects.filter(service=None,is_deleted=False)).exists():
        for question in questions:
            if (options := Options.objects.filter(question=question, is_deleted=False)).exists():
                serialized_data = OptionSerializer(options, context={'request': request}, many=True).data
                question_data = {
                    "question": question.question,
                    "question_id": question.pk,
                    "options": serialized_data,
                }
                list_data.append(question_data)
            else:
                list_data.append({
                    "question": question.question,
                    "options": []
                })

        response_data = {
            "StatusCode": 6000,
            "data": {
            "Questions":list_data
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Failed",
                "Message": "Not Found"
            }
        }
    return Response({'app_data': response_data})



@api_view(['GET'])
@permission_classes([AllowAny])
def search_all(request):
    try:
        q =  request.GET.get('q')
        if q:
            courses = Course.objects.filter(is_deleted=False).distinct('course_name')
            universities = University.objects.filter(is_deleted=False).distinct('university_name')
            
            university_results = universities.filter(Q(university_name__icontains=q))
            course_results = courses.filter(Q(course_name__icontains=q))
            if university_results:
                serialized_data = SearchUniversitySerializer(
                    university_results,
                    context = {"request": request},
                    many=True,
                ).data
            else :
                serialized_data = CourseviewSerializer(
                    course_results,
                    context = {"request": request},
                    many=True,
                ).data

            response_data = {
                "StatusCode": 6000,
                "data": serialized_data
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "data" : {
                    "title" : "Failed",
                    "Message" : "Not Found"
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
def list_count(request):
        university=University.objects.filter(is_deleted=False).distinct('university_name').count()
        course=Course.objects.filter(is_deleted=False).distinct('course_name').count()
        country=Country.objects.filter(is_deleted=False).distinct('country').count()
        student=StudentRecord.objects.filter(is_deleted=False).count()
        if university or course or country:
            response_data={
                "StatusCode":6000,
                "data":{
                    "university_count":university,
                    "course_count":course,
                    "country":country,
                    "student":student
                }
            }
        else:
            response_data={
                "StatusCode":6001,
                "data":[]
            }
     
        return Response({'app_data':response_data})



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_alumnitalk(request):
        name=request.POST['name']
        review=request.POST['review']
        rating=request.POST['rating']
        university=request.POST['university']
        if (university_data:=University.objects.filter(pk=university,is_deleted=False)).exists():
            university=university_data.latest('id')
            student_review=AlumniTalk.objects.create(university=university,
                                                        name=name,
                                                        review=review,
                                                        rating=rating)
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
@group_required(['ezgrad_admin'])
def view_alumnitalk(request):
     if (student:=AlumniTalk.objects.filter(is_deleted=False)).exists():
          serialized_data=AlumniTalkSerializer(student,
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_alumnitalk(request,id):
     if (student:=AlumniTalk.objects.filter(id=id,is_deleted=False)).exists():
          serialized_data=AlumniTalkSerializer(student,
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



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def edit_alumnitalk(request,id):
    if (alumni:=AlumniTalk.objects.filter(id=id,is_deleted=False)).exists():
        alumni=alumni.latest('id')
        name=request.data.get('name')
        review=request.data.get('review')
        rating=request.data.get('rating')
        university=request.data.get('university')
        if name:
            alumni.name=name
        if review:
            alumni.review=review
        if rating:
            alumni.rating=rating
        if university:
            u=University.objects.get(id=university,is_deleted=False)
            alumni.university=u
        alumni.save()
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
    return Response({'app_data':response_data})
            
                             

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_alumnitalk(request,id):
    if (alumni:=AlumniTalk.objects.filter(id=id,is_deleted=False)).exists():
        alumni=alumni.latest('id')
        alumni.is_deleted=True
        alumni.save()
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



@api_view(['GET'])
@permission_classes([AllowAny])
def list_alumnitalk(request,pk):
     if (student:=AlumniTalk.objects.filter(university=pk,is_deleted=False)).exists():
          serialized_data=AlumniTalkSerializer(student,
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

    




        









        







        

        
        











    
      

