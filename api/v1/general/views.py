from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from general.models import ChiefProfile,Countries
from api.v1.general.serializers import ChiefProfileSerializer,ListCountriesSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from general.functions import generate_serializer_errors,check_username,randomnumber
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
# from general.encryption import encrypt, decrypt
from rest_framework import status
import requests
import json
from general.decorators import group_required
from django.db.models import Q

@api_view(['POST'])
@permission_classes([AllowAny])
def create_chief_user(request):
    serialized_data=ChiefProfileSerializer(data=request.data)
    if serialized_data.is_valid():
        username=request.data['username']
        password=request.data['password']
        confirm_password=request.data['confirm_password']
        if password==confirm_password:
            set_password=password
            if not ChiefProfile.objects.filter(username=username,password=password).exists():
                 user = User.objects.create_user(
                            username=username,
                            password=password
                        ) 
                 chief_user= ChiefProfile.objects.create(username=username,
                                        password=password,
                                        user=user
                                        )
                 group_name='ezgrad_admin'
                 chief_group, created = Group.objects.get_or_create(name=group_name)
                 chief_group.user_set.add(user)
                 group_name='ezgrad_admin'
                 response_data={
                     "StatusCode":6000,
                     "data":{
                         "title":"Success",
                         "Message":"Chief user created successfully"
                     }
                 }
            else:
                response_data={
                    "StatusCode":6001,
                    "data":{
                        "title":"Failed",
                        "Message":"Chief user already exist"
                    }
                }
        else:
            response_data={
                "StatusCode":6001,
                "data":{
                    "title":"Failed",
                    "Message":"password didn't Match"
                }
            }
    else:
        response_data={
            "StatusCode":6001,
            "data":{
                "title":"Validation error",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})


@api_view(['POST'])
@permission_classes([AllowAny])
def chief_login(request):
    serialized_data=ChiefProfileSerializer(data=request.data)
    if serialized_data.is_valid():
        username=request.data['username']
        password=request.data['password']
        if ChiefProfile.objects.filter(username=username,is_deleted=False).exists():
            profile=ChiefProfile.objects.get(username=username,is_deleted=False)
            if profile.password==password:
                protocol="http://"
                if request.is_secure():
                    protocol="https://"
                web_host = request.get_host()
                request_url = protocol + web_host + "/api/token/"
                login_response = requests.post(
                        request_url,
                        data={
                            'username': profile.user.username,
                            'password': password,
                        }
                    )
                if login_response.status_code == 200:
                        login_response = login_response.json()

                        response_data = {
                            "StatusCode": 6000,
                            "data" : {
                                "title": "Success!",
                                "message": "Success!",
                                "access_token": login_response["access"],
                                "refresh_token": login_response["refresh"],
                            },
                        }
                else:
                        response_data = {
                            "StatusCode": 6001,
                            "data" : {
                                "title": "Failed!",
                                "message": "Token generation failed",
                                "login_status_code" :  login_response.status_code
                            },
                        }
            else:
                    response_data = {
                        "StatusCode": 6001,
                        "data" : {
                            "title": "Failed",
                            "message": "Password is incorrect",
                        },
                    }
        else:
                response_data = {
                    "StatusCode": 6001,
                    "data" : {
                        "title": "Failed",
                        "message": "User Not Exists"
                    },
                }
    else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Validation Error",
                    "message": generate_serializer_errors(serialized_data._errors)
                }
            }
    return Response({'app_data' : response_data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def list_all_countries(request):
    q = request.GET.get('q') 
    countries = Countries.objects.filter(is_active=True)

    if countries.exists():
        if q:
            countries = countries.filter(Q(name__icontains=q) | Q(phone_code__icontains=q))
        serialized_data = ListCountriesSerializer(countries, many=True).data
        response_data = {
            "StatusCode": 6000,
            "data": serialized_data
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



