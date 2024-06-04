from django.urls import path
from api.v1.student import views

urlpatterns=[

    path('general-search/',views.general_search),
    path('calculate-age/',views.calculate_age),
    path('register-student/',views.register_student),
    path('view-studentprofile/',views.view_studentprofile),
    path('edit-studentprofile/<pk>',views.edit_studentprofile),
    path('delete-studentprofile/<pk>',views.delete_studentprofile),
    path('list-studentdetails/<pk>',views.list_studentdetails),
    path('list-studentprofile/<pk>',views.list_studentprofile),
    path('update-selected-option/<pk>',views.update_selected_option),
    path('save-student-review/<pk>',views.save_student_review),
    path('list-student-review/<pk>',views.list_student_review),
    path('bulk-remove-register-student/',views.bulk_remove_register_student),
    
   

    path('add-student-record/',views.add_student_record),
    path('edit-student-record/<int:pk>',views.edit_student_record),
    path('list-student-documents/',views.list_student_documents),
    path('list-student-record/',views.list_student_record),
    path('notification-status/<pk>',views.notification_status),
    path('view-student-record/',views.view_student_record),
    path('view-single-student-record/<pk>',views.view_single_student_record),
    path('update-university-status-approved/<int:id>',views.update_university_status_approved),
    path('update-university-status-rejected/<int:id>',views.update_university_status_rejected),
    path('bulk-remove-student-record/',views.bulk_remove_student_record),


    path('add-wishlist/',views.add_wishlist),
    path('list-wishlist/',views.list_wishlist),
    path('remove-wishlist/',views.remove_wishlist),
   
    path('login-email/',views.login_email),
    path('login-otp/',views.login_otp),

    
    path('student-login/',views.student_login),
    path('add-answer/',views.add_answer),
    path('filter-university/',views.filter_university),
    path('suggest-filter-university/',views.suggest_filter_university),
    path('specialization-filter-university/',views.specialization_filter_university),
    path('view-answer/',views.view_answer),
    path('delete-answer/<int:id>',views.delete_answer),
    # path('login/',views.UserLogin),

    path('count-enquiry/',views.count_enquiry),
    path('count-student-record/',views.count_student_record),
    path('count-pending-application/',views.count_pending_application),
    path('count-completed-student/',views.count_completed_student),
    path('count-rejected-application/',views.count_rejected_application),

    path('add-enquiry/',views.add_enquiry),
    path('view-enquiry/',views.view_enquiry),
    path('delete-enquiry/<int:id>',views.delete_enquiry),
    path('enquiry-read/<int:id>',views.enquiry_read),

    path('admin-add-student/',views.admin_add_student),
    path('admin-add-answer/',views.admin_add_answer),
    path('admin-filter-university/',views.admin_filter_university),
    
    path('add-suggetions/',views.SuggestedCollageAPIView.as_view()),
    path('suggetions/',views.SuggestedCollageAPIView.as_view()),



]