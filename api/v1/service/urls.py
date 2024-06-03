from django.urls import path
from api.v1.service import views

urlpatterns=[
    path('add-service/',views.add_service),
    path('view-service/',views.view_service),
    path('view-single-service/<pk>',views.view_single_service),
    path('edit-service/<pk>',views.edit_service),
    path('delete-service/<pk>',views.delete_service),
    path('list-service/',views.list_service),

    path('add-coursetype/',views.add_coursetype),
    path('view-coursetype/',views.view_coursetype),
    path('view-single-coursetype/<int:id>',views.view_single_coursetype),
    path('edit-coursetype/<int:id>',views.edit_coursetype),
    path('delete-coursetype/<int:id>',views.delete_coursetype),
    path('list-coursetype/',views.list_coursetype),
    path('view-service-coursetype/',views.view_service_coursetype),
    


    # path('test/',views.test),

  

]