from django.urls import path
from api.v1.general import views


urlpatterns=[

    path('create-chief-user/',views.create_chief_user),
    path('chief-login/',views.chief_login),
    path('list-all-countries/',views.list_all_countries),
    
   
    # path('login/',views.UserLogin),
  

]