from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from web.models import *
from api.v1.web.serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from general.functions import generate_serializer_errors
from general.decorators import group_required
from rest_framework import status
import requests
import traceback
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import json

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_mainbanner(request):
    serialized_data=AddMainBannerSerializer(data=request.data)
    if serialized_data.is_valid():
        main_banner=request.data['main_banner']
        banner_url=request.data['main_banner_url']
        content=request.data['content']
        b=MainBanner.objects.create(main_banner=main_banner,
                                    main_banner_url=banner_url,
                                    content=content)
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Successfully added"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_mainbanner(request):
    if (homedetails:=MainBanner.objects.filter(is_deleted=False)).exists():
        serialized_data=MainBannerSerializer(homedetails,
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
def view_single_mainbanner(request,id):
    if (homedetails:=MainBanner.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=MainBannerSerializer(homedetails,
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
def edit_mainbanner(request,id):
    banner=request.data.get('main_banner')
    banner_url=request.data.get('main_banner_url')
    if (home:=MainBanner.objects.filter(id=id,is_deleted=False)).exists():
        homedata=home.latest('id')
        if banner:
            homedata.main_banner=banner
        if banner_url:
            homedata.main_banner_url=banner_url
        homedata.save()
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Edited Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_mainbanner(request,id):
    if (home:=MainBanner.objects.filter(id=id,is_deleted=False)).exists():
        homedetails=home.latest('id')
        homedetails.is_deleted=True
        homedetails.save()
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not found"
            }
        }
    return Response({'app_data':response_data})

@api_view(['POST'])
@group_required(['ezgrad_admin'])
def hide_mainbanner(request,id):
    if (banner:=MainBanner.objects.filter(id=id,is_deleted=False)).exists():
        m=banner.latest('id')
        m.status=not m.status
        m.save()
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
@permission_classes([AllowAny])
def list_mainbanner(request):
    if (homedetails:=MainBanner.objects.filter(is_deleted=False,status=True)).exists():
        serialized_data=MainBannerSerializer(homedetails,
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
def add_subbanner(request):
    serialized_data=AddSubBannerSerializer(data=request.data)
    if serialized_data.is_valid():
        sub_banner=request.data['sub_banner']
        title=request.data['title']
        content=request.data['content']
        subbanner=Subbanner.objects.create(sub_banner=sub_banner,
                                           title=title,
                                           content=content)
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
def view_subbanner(request):
    if (banner:=Subbanner.objects.filter(is_deleted=False)).exists():
        serialized_data=SubbannerSerializer(banner,
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
def view_single_subbanner(request,id):
    if (banner:=Subbanner.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=SubbannerSerializer(banner,
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
def edit_subbanner(request,id):
    sub_banner=request.data.get('sub_banner')
    title=request.data.get('title')
    content=request.data.get('content')
    if (banner:=Subbanner.objects.filter(id=id,is_deleted=False)).exists():
        subbanner=banner.latest('id')
        if sub_banner:
            subbanner.sub_banner=sub_banner
        if title:
            subbanner.title=title
        if content:
            subbanner.content=content
        subbanner.save()
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
def delete_subbanner(request,id):
    if (banner:=Subbanner.objects.filter(id=id,is_deleted=False)).exists():
        subbanner=banner.latest('id')
        subbanner.is_deleted=True
        subbanner.save()
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
def list_subbanner(request):
    if (banner:=Subbanner.objects.filter(is_deleted=False)).exists():
        serialized_data=SubbannerSerializer(banner,
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
            "Statucode":6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})
    


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def edit_contact(request):
    serialized_data=AddContactSerializer(data=request.data)
    if serialized_data.is_valid():
        about=request.data['about']
        address=request.data['address']
        phone=request.data['phone']
        email=request.data['email']
        facebook_url=request.data['facebook_url']
        instagram_url=request.data['instagram_url']
        youtube_url=request.data['youtube_url']
        whatsapp_url=request.data['whatsapp_url']
        linkedln_url=request.data['linkedln_url']
        if Contact.objects.exists():
            contact=Contact.objects.first()
            if about:
                contact.about=about
            if address:
                contact.address=address
            if phone:
                contact.phone=phone
            if email:
                contact.email=email
            if facebook_url:
                contact.facebook_url=facebook_url
            if instagram_url:
                contact.instagram_url=instagram_url
            if youtube_url:
                contact.youtube_url=youtube_url
            if whatsapp_url:
                contact.whatsapp_url=whatsapp_url
            if linkedln_url:
                contact.linkedln_url=linkedln_url
            contact.save()
            response_data={
                     "StatusCode" : 6000,
                     "data":{
                            "title": "success",
                            "message":"Upated Successfully"
                     }    
              }
        else:
            contact=Contact.objects.create(about=about,
                                        address=address,
                                        phone=phone,
                                        email=email,
                                        facebook_url=facebook_url,
                                        instagram_url=instagram_url,
                                        youtube_url=youtube_url,
                                        whatsapp_url=whatsapp_url,
                                        linkedln_url=linkedln_url
                                        )
            response_data={
                "StatusCode" : 6000,
                "data":{
                    "title":"Success",
                    "Message":"Successfully Added"
                }
            }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_contact(request):
    if (contact:=Contact.objects.filter(is_deleted=False)).exists():
        serialized_data=ContactSerializer(contact,
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
def list_contact(request):
    if (contact:=Contact.objects.filter(is_deleted=False)).exists():
        contact_data=contact.latest('id')
        serialized_data=ContactSerializer(contact_data,
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
    return Response({'app-data':response_data})


@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_details(request):
    serialized_data=AddDetailSerializer(data=request.data)
    if serialized_data.is_valid():
        image=request.data['image']
        title=request.data['title']
        content=request.data['content']
        details=Details.objects.create(image=image,title=title,content=content)
        response_data={
            "StatusCode" : 6000,
            "data":
            {
                "title":"Success",
                "Message":"Added Successfully"
            
            }
        }
    else:
        response_data={
             "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_details(request):
    if (details:=Details.objects.filter(is_deleted=False)).exists():
        serialized_data=DetailSerializer(details,
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
def edit_details(request,id):
    title=request.data.get('title')
    content=request.data.get('content')
    image=request.data.get('image')
    if (details:=Details.objects.filter(id=id,is_deleted=False)).exists():
        D=details.latest('id')
        if title:
            D.title=title
        if content:
            D.content=content
        if image:
            D.image=image
        D.save()
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Edited Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})

    
@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_details(request,id):
    if (d:=Details.objects.filter(id=id,is_deleted=False)).exists():
        details=d.latest('id')
        details.is_deleted=True
        details.save()
        response_data={
             "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
             "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_details(request):
    if (details:=Details.objects.filter(is_deleted=False)).exists():
        serialized_data=DetailSerializer(details,
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
def add_experts(request):
    serialized_data=AddExpertSerializer(data=request.data)
    if serialized_data.is_valid():
        name=request.data['name']
        role=request.data['role']
        experience=request.data['experience']
        photo=request.data['photo']
        rating=request.data['rating']
        counselling=request.data['counselling']
        exp=Experts.objects.create(
            name=name,
            role=role,
            experience=experience,
            photo=photo,
            rating=rating,
            counselling=counselling,
        )
        response_data={
             "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Added Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":
            {
                "title":"Failed",
                "Message":generate_serializer_errors(serialized_data._errors)
            }
        }
    return Response({'app_data':response_data})



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_experts(request):
    q = request.GET.get('q')
    if (expert := Experts.objects.filter(is_deleted=False)).exists():
            if q:
                exp = expert.filter(
                    Q(name__icontains=q) | 
                    Q(role__icontains=q) | 
                    Q(experience__icontains=q) |  
                    Q(rating__icontains=q)
                )
            
                serialized_data=ExpertSerializer(exp,
                                                context={
                                                    "request":request,
                                                },
                                                many=True,).data
                response_data={
                    "StatusCode":6000,
                    "data":serialized_data
                }
            else:
                serialized_data=ExpertSerializer(expert,
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
def view_single_experts(request,id):
    if (expert:=Experts.objects.filter(id=id,is_deleted=False)).exists():
        serialized_data=ExpertSerializer(expert,
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
def edit_experts(request,id):
    name=request.data.get('name')
    role=request.data.get('role')
    experience=request.data.get('experience')
    photo=request.data.get('photo')
    rating=request.data.get('rating')
    counselling=request.data.get('counselling')
    if (exp:=Experts.objects.filter(id=id,is_deleted=False)).exists():
        expert=exp.latest('id')
        if name:
            expert.name=name
        if role:
            expert.role=role
        if experience:
            expert.experience=experience
        if photo:
            expert.photo=photo
        if rating:
            expert.rating=rating
        if counselling:
            expert.counselling=counselling
        expert.save()
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Edited Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})



@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_experts(request,id):
    if (exp:=Experts.objects.filter(id=id,is_deleted=False)).exists():
        expert=exp.latest('id')
        expert.is_deleted=True
        expert.save()
        response_data={
            "StatusCode" : 6000,
            "data":{
                "title":"Success",
                "Message":"Deleted Successfully"
            }
        }
    else:
        response_data={
            "StatusCode" : 6001,
            "data":{
                "title":"Failed",
                "Message":"Not Found"
            }
        }
    return Response({'app_data':response_data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_experts(request):
    if (experts:=Experts.objects.filter(is_deleted=False)).exists():
        serialized_data=ExpertSerializer(experts,
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
def bulk_remove_experts(request):
    expert=Experts.objects.all()
    if expert.exists():
        expert.update(is_deleted=True)
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
        
    

# @api_view(['POST'])
# @group_required(['ezgrad_admin'])
# def add_student_testimonials(request):
#     serialized_data=AddStudentTestimonialSerializer(data=request.data)
#     if serialized_data.is_valid():
#         image=request.data['image']
#         university=request.data['university']
#         testimonial=StudentTestimonials.objects.create(image=image,
#                                                        university=university)
#         response_data={
#             "StatusCode":6000,
#             "data":{
#                 "title":"Success",
#                 "Message":"Added Successfully"
#             }
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})


# @api_view(['GET'])
# @group_required(['ezgrad_admin'])
# def view_student_testimonials(request):
#     if (testimonial:=StudentTestimonials.objects.filter(is_deleted=False)).exists():
#         serialized_data=StudentTestimonialSerializer(testimonial,
#                                                      context={
#                                                          "request":request,
#                                                      },many=True,).data
#         response_data={
#             "StatusCode":6000,
#             "data":serialized_data
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})


# @api_view(['PUT'])
# @group_required(['ezgrad_admin'])
# def edit_student_testimonials(request,id):
#     image=request.data.get('image')
#     university=request.data.get('university')
#     if (testimonial:=StudentTestimonials.objects.filter(id=id,is_deleted=False)).exists():
#         testimonials=testimonial.latest('id')
#         if image:
#             testimonials.image=image
#         if university:
#             testimonials.university=university
#         testimonials.save()
#         response_data={
#             "StatusCode":6000,
#             "data":{
#                 "title":"Success",
#                 "Message":"Updated Successfully"
#             }
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})
        

# @api_view(['DELETE'])
# @group_required(['ezgrad_admin'])
# def delete_student_testimonials(request,id):
#     if (testimonials:=StudentTestimonials.objects.filter(id=id,is_deleted=False)).exists():
#         testimonial=testimonials.latest('id')
#         testimonial.is_deleted=True
#         testimonial.save()
#         response_data={
#             "StatusCode":6000,
#             "data":{
#                 "title":"Success",
#                 "Message":"Deleted Successfully"
#             }
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def list_student_testimonials(request):
#     if (testimonial:=StudentTestimonials.objects.filter(is_deleted=False)).exists():
#         serialized_data=StudentTestimonialSerializer(testimonial,
#                                                      context={
#                                                          "request":request,
#                                                      },many=True,).data
#         response_data={
#             "StatusCode":6000,
#             "data":serialized_data
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})


# @api_view(['DELETE'])
# @group_required(['ezgrad_admin'])
# def bulk_remove_student_testimonials(request):
#     student=StudentTestimonials.objects.all()
#     if student.exists():
#         student.update(is_deleted=True)
#         response_data={
#             "StatusCode":6000,
#             "data":{
#                 "title":"Success",
#                 "Message":"Deleted Successfully"
#             }
#         }
#     else:
#         response_data={
#             "StatusCode":6001,
#             "data":{
#                 "title":"Failed",
#                 "Message":"Not Found"
#             }
#         }
#     return Response({'app_data':response_data})



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_blog(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateBlogSerializer(data=request.data)

        if serialized_data.is_valid():
            title = request.data['title']
            description = request.data['description']
            image=request.data.get('image')
            video = request.data.get('video')
            slug=request.data.get('slug')
            renamed_slug=slug.replace(' ','-')   
            blog_date=request.data.get('blog_date')         
            tag_ids = request.data.getlist('tag_ids')
            category_ids = request.data.getlist('category_ids')
            if not Blogs.objects.filter(title=title,slug=renamed_slug, is_deleted=False).exists():
                blog = Blogs.objects.create(
                    title = title,
                    description = description,
                    image = image,
                    video = video,
                    slug=renamed_slug,
                    blog_date=blog_date
                )
                tag_id=tag_ids
                for i in tag_id:
                    tag=Tags.objects.get(pk=i)
                b=blog.tags.add(tag)
                category=category_ids
                for category_id in category:
                    c = Category.objects.get(pk=category_id)
                b=blog.category.add(c)

                transaction.commit()
                response_data = {
                   "StatusCode" : 6000,
                   "data" : {
                       "title" : "Success",
                       "message" : "Blog created successfully"
                   }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Blog already exists"
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
@group_required(['ezgrad_admin'])
def view_blog(request):
    try:
        transaction.set_autocommit(False)
        if (blog := Blogs.objects.filter(is_deleted=False)).exists():
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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



@api_view(['GET'])
@group_required(['ezgrad_admin'])
def view_single_blog(request,pk):
    try:
        transaction.set_autocommit(False)
        if (blog := Blogs.objects.filter(pk=pk,is_deleted=False)).exists():
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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
@group_required(['ezgrad_admin'])
def edit_blog(request,pk):
    try:
        transaction.set_autocommit(False)
        if (blog:=Blogs.objects.filter(pk=pk,is_deleted=False)).exists():
            blog=blog.latest('id')
            title = request.data.get('title')
            description = request.data.get('description')
            image = request.data.get('image')
            video = request.data.get('video')
            tags = request.data.getlist('tags')
            category = request.data.getlist('category')
            slug = request.data.get('slug')
            blog_date = request.data.get('blog_date')

            if title:
                blog.title=title
            if description:
                blog.description=description
            if image:
                blog.image=image
            if video:
                blog.video=video
            if blog_date:
                blog.blog_date=blog_date
            if tags:
                for tag_id in tags:
                    tag = Tags.objects.get(pk=tag_id)
                    blog.tags.add(tag)
            if category:
                for c_id in category:
                    categories = Category.objects.get(pk=c_id)
                    blog.category.add(categories)
            if slug:
                  renamed_slug=slug.replace(' ','-')
                  if (p:=Blogs.objects.filter(is_deleted=False,slug=renamed_slug)).exclude(id=blog.id).exists():
                            response_data = {
                            "StatusCode" : 6001,
                            "data" : {
                                   "title" : "Failed",
                                   "message" : "Slug Already Exist"
                            }
                            }
                            return Response(response_data)
                  else:
                    blog.slug=renamed_slug
            blog.save()
            transaction.commit()

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


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_blog(request,pk):
    try:
        transaction.set_autocommit(False)
        if (blog:=Blogs.objects.filter(pk=pk,is_deleted=False)).exists():
            blog=blog.latest('id')
            blog.is_deleted=True
            blog.save()
            transaction.commit()
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
def list_blog(request):
    try:
        transaction.set_autocommit(False)
        if (blog := Blogs.objects.filter(is_deleted=False)).exists():
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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



@api_view(['GET'])
@permission_classes([AllowAny])
def list_recent_blog(request):
    try:
        transaction.set_autocommit(False)
        blog = Blogs.objects.filter(is_deleted=False).order_by('-blog_date')
        if blog:
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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

@api_view(['GET'])
@permission_classes([AllowAny])
def list_featured_blog(request):
    try:
        transaction.set_autocommit(False)
        if (blog := Blogs.objects.filter(featured=True,is_deleted=False)).exists():
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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



@api_view(['GET'])
@permission_classes([AllowAny])
def list_single_blog(request,slug):
    try:
        transaction.set_autocommit(False)
        if (blog := Blogs.objects.filter(slug=slug,is_deleted=False)).exists():
            serialized_data = ListBlogSerializer(
                blog,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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



@api_view(['GET'])
@permission_classes([AllowAny])
def search_blog(request):
    search_data = request.GET.get('q')

    if search_data is not None:
        blog = Blogs.objects.filter(Q(title__icontains=search_data) | Q(description__icontains=search_data), is_deleted=False)

        if blog:
            serialized_data = ListBlogSerializer(
                blog,
                context={'request': request},
                many=True
            ).data
           
            page_number = request.GET.get("page") 
            items_per_page = 4
            paginator = Paginator(serialized_data, items_per_page)
            try:
                page_obj = paginator.page(page_number)
                response_data = {
                    "StatusCode": 6000,
                    "data": {
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'page_number': page_number,
                        'results': page_obj.object_list,
                    }
                }
            except EmptyPage:
                        instances = paginator.page(1)
                        response_data = {
                                "StatusCode": 6000,
                                "data":
                                {
                                    'count': paginator.count,
                                    'num_pages': paginator.num_pages,
                                    'page_number': 1,
                                    'results':instances.object_list,
                                } 
                                
                        }
            except PageNotAnInteger:
                        instances= paginator.page(1)
                        response_data = {
                                "StatusCode": 6000,
                                "data": {
                                'count': paginator.count,
                                'num_pages': paginator.num_pages,
                                'page_number': 1,
                                'results': instances.object_list,
                                
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
    else:
        response_data = {
            "StatusCode": 6002,
            "data": {
                "title": "Failed",
                "Message": "Search query is empty"
            }
        }

    return Response({'app_data': response_data})
 
@api_view(['GET'])
@permission_classes([AllowAny])
def list_categories(request):
    if (c:=Category.objects.filter(is_deleted=False)).exists():
        serialized_data=CategorySerializer(c,
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
def list_tags(request):
    if (c:=Tags.objects.filter(is_deleted=False)).exists():
        serialized_data=TagSerializer(c,
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
def list_category_blog(request,pk):
    category=request.GET.get('category')
    if (blog:=Blogs.objects.filter(category=pk,is_deleted=False)).exists():
        serialized_data=ListBlogSerializer(blog,
                                           context={
                                               "request":request,
                                           },many=True,).data
        page_number = request.GET.get("page") 
        items_per_page = 6
        paginator = Paginator(serialized_data, items_per_page)
        try:
            page_obj = paginator.page(page_number)
            response_data = {
                "StatusCode": 6000,
                "data": {
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'page_number': page_number,
                    'results': page_obj.object_list,
                }
            }
        except EmptyPage:
                    instances = paginator.page(1)
                    response_data = {
                            "StatusCode": 6000,
                            "data":
                            {
                                'count': paginator.count,
                                'num_pages': paginator.num_pages,
                                'page_number': 1,
                                'results':instances.object_list,
                            } 
                            
                    }
        except PageNotAnInteger:
                    instances= paginator.page(1)
                    response_data = {
                            "StatusCode": 6000,
                            "data": {
                            'count': paginator.count,
                            'num_pages': paginator.num_pages,
                            'page_number': 1,
                            'results': instances.object_list,
                            
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
def list_tag_blog(request,pk):
    tag=request.GET.get('tag')
    if (blog:=Blogs.objects.filter(tags=pk,is_deleted=False)).exists():
        serialized_data=ListBlogSerializer(blog,
                                           context={
                                               "request":request,
                                           },many=True,).data
        page_number = request.GET.get("page") 
        items_per_page = 6
        paginator = Paginator(serialized_data, items_per_page)
        try:
            page_obj = paginator.page(page_number)
            response_data = {
                "StatusCode": 6000,
                "data": {
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'page_number': page_number,
                    'results': page_obj.object_list,
                }
            }
        except EmptyPage:
                    instances = paginator.page(1)
                    response_data = {
                            "StatusCode": 6000,
                            "data":
                            {
                                'count': paginator.count,
                                'num_pages': paginator.num_pages,
                                'page_number': 1,
                                'results':instances.object_list,
                            } 
                            
                    }
        except PageNotAnInteger:
                    instances= paginator.page(1)
                    response_data = {
                            "StatusCode": 6000,
                            "data": {
                            'count': paginator.count,
                            'num_pages': paginator.num_pages,
                            'page_number': 1,
                            'results': instances.object_list,
                            
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
def create_comment(request, pk):
    try:
        transaction.set_autocommit(False)
        serialized_data = CreateCommentSerializer(data=request.data)


        if serialized_data.is_valid():
            comment = request.data["comment"]
            name = request.data["name"]
            email = request.data["email"]
            phone = request.data.get('phone')

            if (blog := Blogs.objects.filter(pk=pk, is_deleted=False)).exists():
                blog = blog.latest("id")

                comment = BlogComment.objects.create(
                    blog = blog,
                    comment = comment,
                    name = name,
                    email = email,
                    phone=phone
                )

                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Success",
                        "message" : "Comment added successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Blog not found"
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

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def list_comment(request,pk):
    try:
        if (comment := BlogComment.objects.filter(blog=pk,is_active=True)).exists():
            comment = comment.order_by("-date_added")

            serialized_data = ListCommentSerializer(
                comment,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
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

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@group_required(['ezgrad_admin'])
def add_career(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddCareerSerializer(data=request.data)

        if serialized_data.is_valid():
            job_title = request.data['job_title']
            job_description = request.data['job_description']
            description = request.data['description']
            job_mode = request.data['job_mode']
            job_type = request.data['job_type']
            date_added = request.data.get('date_added')
            career = Careers.objects.create(
                job_title=job_title,
                job_description=job_description,
                description=description,
                job_mode=job_mode,
                job_type=job_type,
                date_added=date_added, 
                )
            
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Created successfully"
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
@group_required(['ezgrad_admin'])
def view_career(request):
    try:
        transaction.set_autocommit(False)
        if (career := Careers.objects.filter(is_deleted=False)).exists():
            serialized_data = CareerSerializer(
                career,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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
@group_required(['ezgrad_admin'])
def edit_career(request,pk):
    try:
        transaction.set_autocommit(False)
        if (career:=Careers.objects.filter(pk=pk,is_deleted=False)).exists():
            career=career.latest('id')
            job_title=request.data.get('job_title')
            job_description=request.data.get('job_description')
            description=request.data.get('description')
            job_mode=request.data.get('job_mode')
            job_type=request.data.get('job_type')
            date_added=request.data.get('date_added')
            if job_title:
                career.job_title=job_title
            if job_description:
                career.job_description=job_description
            if description:
                career.description=description
            if job_mode:
                career.job_mode=job_mode
            if job_type:
                career.job_type=job_type
            if date_added:
                career.date_added=date_added

            career.save()
            transaction.commit()

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


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_career(request,pk):
    try:
        transaction.set_autocommit(False)
        if (career:=Careers.objects.filter(pk=pk,is_deleted=False)).exists():
            career=career.latest('id')
            career.is_deleted=True
            career.save()
            transaction.commit()
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
def list_career(request):
    try:
        transaction.set_autocommit(False)
        if (career := Careers.objects.filter(is_deleted=False)).exists():
            serialized_data = CareerSerializer(
                career,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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





@api_view(['GET'])
@permission_classes([AllowAny])
def list_hiring(request):
    try:
        transaction.set_autocommit(False)
        if (career := Careers.objects.filter(is_deleted=False,hiring=True)).exists():
            serialized_data = CareerSerializer(
                career,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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
def apply_job(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = AddCareerApplySerializer(data=request.data)

        if serialized_data.is_valid():
            name = request.data['name']
            phone = request.data['phone']
            email = request.data.get('email')
            cv = request.data.get('cv')
            apply_for=request.data.get('apply_for')
            if(career:=Careers.objects.filter(id=apply_for,is_deleted=False)).exists():
                career=career.latest('id')
                career_apply = CareerApply.objects.create(
                name=name,
                phone=phone,
                email=email,
                cv=cv,
                apply_for=career, 
                )
            
            transaction.commit()
            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "message" : "Created successfully"
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
@group_required(['ezgrad_admin'])
def view_apply_job(request):
    try:
        transaction.set_autocommit(False)
        if (career := CareerApply.objects.filter(is_deleted=False)).exists():
            serialized_data = CareerApplySerializer(
                career,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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


@api_view(['DELETE'])
@group_required(['ezgrad_admin'])
def delete_apply_job(request,pk):
    try:
        transaction.set_autocommit(False)
        if (career:=CareerApply.objects.filter(pk=pk,is_deleted=False)).exists():
            career=career.latest('id')
            career.is_deleted=True
            career.save()
            transaction.commit()
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
def list_checklist(request):
    try:
        transaction.set_autocommit(False)
        if (checklist := Checklist.objects.filter(is_deleted=False)).exists():
            serialized_data = ChecklistSerializer(
                checklist,
                context = {
                    "request": request
                },
                many=True
            ).data

            response_data ={
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data ={
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

from datetime import date

class PlacedStudentAPIView(APIView):
    @group_required(['ezgrad_admin'])
    def post(self,request):
        data = request.data.copy()
        if 'profile_image' not in data or data['profile_image'] == "":
            data['profile_image'] = None
        if 'year' not in data or data['year'] == "":
            data['year'] = date.today().isoformat()
        serializer = PlacedStudentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data,
                    "Message": "Placed Student Added"
                }
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": serializer.errors
                }
            }
        return Response({'app_data':response_data})
    def get(self,request,id=None):
        try:
            if id:
                instance = PlacedStudent.objects.filter(id=id,is_deleted=False)
                serializer = PlacedStudentSerializer(instance,many=True)
            else:
                instance = PlacedStudent.objects.filter(is_deleted=False)
                serializer = PlacedStudentSerializer(instance,many=True,context={'request': self.request})
            response_data = {
                    "StatusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": serializer.data,
                        "Message": "Placed Student list"
                    }
                }
        except:
            response_data = {
                "StatusCode": 6001,
                "data": {
                    "title": "Error",
                    "Message": serializer.errors
                }
            }
        return Response({'app_data':response_data})
    
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
            if 'image' not in data or data['image'] == "" or data['image'] == "undefined":
                data['image'] = instance.image
            serializer = PlacedStudentSerializer(instance, data=data, partial=True)
            print(serializer)
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
    def delete(self,request,id):
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
            instance.is_deleted = True
            instance.save()
            response_data = {
                "StatusCode": 6000,
                "data": {
                    "title": "Success",
                    "Message": "Updated"
                }
            }
        return Response({'app_data': response_data})

    def get_object(self, id):
        try:
            instance = PlacedStudent.objects.filter(id=id, is_deleted=False).first()
            return instance
        except PlacedStudent.DoesNotExist:
            return None


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def test(request):
#     serializer = TestSerializer(data=request.data)

#     if serializer.is_valid():
#         # Save the serializer data directly
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)