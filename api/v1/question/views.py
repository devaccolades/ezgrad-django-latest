from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from student.models import StudentProfile
from service.models import *
from question.models import Questions,Options
from api.v1.question.serializers import AddQuestionSerializer,QuestionsSerializer,AddOptionSerializer,OptionSerializer,ListOptionSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from general.functions import generate_serializer_errors
from general.decorators import group_required
import random


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_question(request):
    serialized_data=AddQuestionSerializer(data=request.data)
    if serialized_data.is_valid():
        service=request.data.get('service')
        question=request.data['question']
        if service:
            if (s:=ServiceType.objects.filter(pk=service,is_deleted=False)).exists():
                s=s.latest('id')
                q=Questions.objects.create(service=s,question=question)
                response_data={
                    "StatusCode":6000,
                    "data":{
                        "title":"Success",
                        "Message":"Successfully Added"
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
            q=Questions.objects.create(question=question)
            response_data={
                "StatusCode":6000,
                "data":{
                    "title":"Success",
                    "Message":"Successfully Added"
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
def view_question(request):
    list_data = []
    questions = Questions.objects.filter(is_deleted=False).order_by('id')
    if questions.exists():
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
                    "question_id":question.pk,
                    "options": []
                })

        response_data = {
            "StatusCode": 6000,
            "data": list_data
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


@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_question(request,id):
    question=request.data.get('question')
    service=request.data.get('service')
    if(questions:=Questions.objects.filter(id=id,is_deleted=False)).exists():
        q=questions.latest('id')
        if question:
            q.question=question
        if service:
            ss=ServiceType.objects.get(id=service,is_deleted=False)
            q.service=ss
        q.save()
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
def delete_question(request,id):
    if(question:=Questions.objects.filter(id=id,is_deleted=False)).exists():
       q=question.latest('id')
       q.is_deleted=True
       q.save()
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
            "Data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_question(request):
    service=request.GET.get('service')
    list_data = []
    if (questions := Questions.objects.filter(service=service,is_deleted=False)).exists():
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
            "data": list_data
            
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



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_options(request):
    serialized_data = AddOptionSerializer(data=request.data)
    if serialized_data.is_valid():
        id=request.data.get('question')
        if (question:=Questions.objects.filter(id=id,is_deleted=False)).exists():
            questions=question.latest('id')
            options=request.data['options']
            option=Options.objects.create(
            question=questions,
            options=options
        )
        response_data={
            "StatusCode":6000,
            "data":{
                "title":"Success",
                "Message":"Successfully Added"
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
def view_options(request):
    response_data = []
    if (questions:=Questions.objects.filter(is_deleted=False)).exists():
    
        for question in questions:
            if (options:=Options.objects.filter(question=question, is_deleted=False)).exists():
                serialized_data = OptionSerializer(options, context={'request': request}, many=True).data
                response_data.append({
                    "question": question.question,
                    "options": serialized_data,
                })
            else:
                response_data.append({
                    "question": question.question,
                    "options": []
                })
    else:
        response_data = []

    return Response({'app_data': response_data})

@api_view(['PUT'])
@group_required(['ezgrad_admin'])
def edit_options(request,pk):
    options=request.data.get('options')
    if(option:=Options.objects.filter(pk=pk,is_deleted=False)).exists():
        opt=option.latest('id')
        if options:
            opt.options=options
        opt.save()
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
def delete_options(request,pk):
    if(option:=Options.objects.filter(pk=pk,is_deleted=False)).exists():
        options=option.latest('id')
        options.is_deleted=True
        options.save()
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
def view_service_options(request,pk):
    if (options:=Options.objects.filter(question__service=pk,is_deleted=False)).exists():

        serialized_data = ListOptionSerializer(options, context={'request': request}, many=True).data
        
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
        
    return Response({'app_data': response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def admin_list_questions(request):
    list_data = []
    if (questions := Questions.objects.filter(is_deleted=False)).exists():
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
            "data": list_data
            
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


