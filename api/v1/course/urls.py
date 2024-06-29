from django.urls import path
from api.v1.course import views

urlpatterns=[

    # path('list-course-specialization/',views.list_course_specialization),
    # path('list-specialization-university/<pk>',views.list_specialization_university),

    path('add-university/',views.add_university),
    path('view-university/',views.view_university),
    path('view-single-university/<pk>',views.view_single_university),
    path('edit-university/<pk>',views.edit_university),
    path('delete-university/<pk>',views.delete_university),
    path('fact-list/',views.fact_list),
    path('list-university-logo/',views.list_university_logo),
    path('list-universitylogo-studentform/',views.list_universitylogo_studentform),
    path('list-popular-university/',views.list_popular_university),
    path('count-university/',views.count_university),
    path('compare-university/',views.compare_university),
    path('list-single-university-details/<pk>',views.list_single_university_details),
    path('list-single-university-fee-details/<pk>',views.list_single_university_fee_details),
    path('add-university-option/<pk>',views.add_university_option),
    path('add-university-accreditation/<pk>',views.add_university_accreditation),
    path('bulk-remove-university/',views.bulk_remove_university),

    

    path('add-facility-type/',views.add_facility_type),
    path('view-facility-type/',views.view_facility_type),
    path('view-single-facility-type/<pk>',views.view_single_facility_type),
    path('edit-facility-type/<pk>',views.edit_facility_type),
    path('delete-facility-type/<pk>',views.delete_facility_type),
  
    path('add-facilities/',views.add_facilities),
    path('view-facilities/<pk>',views.view_facilities),
    path('view-university-facilities/',views.view_university_facilities),
    path('view-single-facilities/<int:id>',views.view_single_facilities),
    path('edit-facilities/<int:id>',views.edit_facilities),
    path('delete-facilities/<int:id>',views.delete_facilities),
    path('list-facilities/<pk>',views.list_facilities),


    path('add-facts/',views.add_facts),
    path('view-facts/',views.view_facts),
    path('view-single-facts/<int:id>',views.view_single_facts),
    path('edit-facts/<int:id>',views.edit_facts),
    path('delete-facts/<int:id>',views.delete_facts),

    path('add-university-image/',views.add_university_image),
    path('view-university-image/',views.view_university_image),
    path('view-single-university-image/<int:id>',views.view_single_university_image),
    path('edit-university-image/<int:id>',views.edit_university_image),
    path('delete-university-image/<int:id>',views.delete_university_image),
    
    path('add-accreditation/',views.add_accreditation),
    path('edit-accreditation/<int:id>',views.edit_accreditation),
    path('view-accreditation/',views.view_accreditation),
    path('view-single-accreditation/<int:id>',views.view_single_accreditation),
    path('delete-accreditation/<int:id>',views.delete_accreditation),
    path('bulk-remove-accreditation/',views.bulk_remove_accreditation),
    
    path('add-accreditation-points/',views.add_accreditation_points),
    path('view-accreditation-points/<int:id>',views.view_accreditation_points),
    path('view-single-accreditation-points/<int:id>',views.view_single_accreditation_points),
    path('edit-accreditation-points/<int:id>',views.edit_accreditation_points),
    path('delete-accreditation-points/<int:id>',views.delete_accreditation_points),

    
    path('add-course/',views.add_course),
    path('add-general-course/',views.add_general_course),
    path('view-course/',views.view_course),
    path('view-course-selection/',views.CourseSelection.as_view()),
    path('view-single-course/<pk>',views.view_single_course),
    path('edit-course/<pk>',views.edit_course),
    path('delete-course/<pk>',views.delete_course),
    path('list-courses/',views.list_courses),
    path('list-courses-suggest/',views.list_courses_suggest),
    path('list-course-country/',views.list_course_country),
    path('list-regular-states/',views.list_regular_states),
    path('list-regular-course-studentform/',views.list_regular_course_studentform),
    path('list-course-studentform/',views.list_course_studentform),
    path('bulk-remove-course/',views.bulk_remove_course),

    path('add-admission-procedure/',views.add_admission_procedure),
    path('view-admission-procedure/<pk>',views.view_admission_procedure),
    path('view-specialization-admission-procedure/<pk>',views.view_specialization_admission_procedure),
    path('view-single-admission-procedure/<int:id>',views.view_single_admission_procedure),
    path('edit-admission-procedure/<int:id>',views.edit_admission_procedure),
    path('delete-admission-procedure/<int:id>',views.delete_admission_procedure),

    path('list-all-courses/',views.list_all_courses),
    path('list-specialization-course-university/',views.list_specialization_course_university),
    path('list-universities-specialization/',views.list_universities_specialization),
    path('search-course/',views.search_course),
    


    path('add-specialization/',views.add_specialization),
    path('view-specialization/',views.view_specialization),
    path('view-single-specialization/<pk>',views.view_single_specialization),
    path('edit-specialization/<pk>',views.edit_specialization),
    path('delete-specialization/<pk>',views.delete_specialization),
    path('list-specialization/',views.list_specialization),
    path('list-specialization-studentform/',views.list_specialization_studentform),
    path('bulk-remove-specialization/',views.bulk_remove_specialization),
    

    path('add-country/',views.add_country),
    path('view-country/',views.view_country),
    path('view-single-country/<int:id>',views.view_single_country),
    path('edit-country/<int:id>',views.edit_country),
    path('delete-country/<int:id>',views.delete_country),
    path('list-country/',views.list_country),
    

    path('add-faq/',views.add_faq),
    path('view-faq/',views.view_faq),
    path('view-single-faq/<int:id>',views.view_single_faq),
    path('edit-faq/<int:id>',views.edit_faq),
    path('delete-faq/<int:id>',views.delete_faq),
    path('list-faq/<pk>',views.list_faq),

    path('add-currency/',views.add_currency),
    path('view-currency/',views.view_currency),
    path('view-single-currency/<int:id>',views.view_single_currency),
    path('edit-currency/<int:id>',views.edit_currency),
    path('list-currency/',views.list_currency),
    path('delete-currency/<int:id>',views.delete_currency),
    path('convert-currency/<int:id>',views.convert_currency),

    path('add-university-banner/',views.add_university_banner),
    path('view-university-banner/',views.view_university_banner),
    path('view-single-university-banner/<int:id>',views.view_single_university_banner),
    path('edit-university-banner/<int:id>',views.edit_university_banner),
    path('delete-university-banner/<int:id>',views.delete_university_banner),
    path('list-university-banner/',views.list_university_banner),

    path('add-placement-partner/',views.add_placement_partner),
    path('edit-placement-partner/<int:id>',views.edit_placement_partner),
    path('view-placement-partner/',views.view_placement_partner),
    path('view-single-placement-partner/<int:id>',views.view_single_placement_partner),
    path('delete-placement-partner/<int:id>',views.delete_placement_partner),
    path('list-placement-partner/<pk>',views.list_placement_partner),


    path('add-university-document/',views.add_university_document),
    path('edit-university-document/<int:id>',views.edit_university_document),
    path('view-university-document/',views.view_university_document),
    path('view-single-university-document/<int:id>',views.view_single_university_document),
    path('delete-university-document/<int:id>',views.delete_university_document),
    path('list-university-document/<pk>',views.list_university_document),

    path('search-university/',views.search_university),
    path('search-courses/',views.search_courses),

    path('add-state/',views.add_state),
    path('edit-state/<int:id>',views.edit_state),
    path('view-state/',views.view_state),
    path('view-single-state/<int:id>',views.view_single_state),
    path('delete-state/<int:id>',views.delete_state),
    path('view-states/<int:id>',views.view_states),
    path('list-states/<int:id>',views.list_states),

    path('suggest-university/',views.suggest_university),
    path('search-all/',views.search_all),
    path('list-count/',views.list_count),

    path('add-alumnitalk/',views.add_alumnitalk),
    path('view-alumnitalk/',views.view_alumnitalk),
    path('view-single-alumnitalk/<int:id>',views.view_single_alumnitalk),
    path('edit-alumnitalk/<int:id>',views.edit_alumnitalk),
    path('delete-alumnitalk/<int:id>',views.delete_alumnitalk),
    path('list-alumnitalk/<pk>',views.list_alumnitalk),



 

   

   
    
 




  

    

]