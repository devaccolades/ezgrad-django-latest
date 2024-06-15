from django.urls import path
from api.v1.web import views

urlpatterns=[
    path('add-mainbanner/',views.add_mainbanner),
    path('view-mainbanner/',views.view_mainbanner),
    path('view-single-mainbanner/<int:id>',views.view_single_mainbanner),
    path('edit-mainbanner/<int:id>',views.edit_mainbanner),
    path('delete-mainbanner/<int:id>',views.delete_mainbanner),
    path('hide-mainbanner/<int:id>',views.hide_mainbanner),
    path('list-mainbanner/',views.list_mainbanner),

    path('add-subbanner/',views.add_subbanner),
    path('view-subbanner/',views.view_subbanner),
    path('view-single-subbanner/<int:id>',views.view_single_subbanner),
    path('edit-subbanner/<int:id>',views.edit_subbanner),
    path('delete-subbanner/<int:id>',views.delete_subbanner),
    path('list-subbanner/',views.list_subbanner),


    path('edit-contact/',views.edit_contact),
    path('view-contact/',views.view_contact),
    path('list-contact/',views.list_contact),

    path('add-details/',views.add_details),
    path('view-details/',views.view_details),
    path('edit-details/<int:id>',views.edit_details),
    path('delete-details/<int:id>',views.delete_details),
    path('list-details/',views.list_details),


    path('add-experts/',views.add_experts),
    path('view-experts/',views.view_experts),
    path('view-single-experts/<int:id>',views.view_single_experts),
    path('edit-experts/<int:id>',views.edit_experts),
    path('delete-experts/<int:id>',views.delete_experts),
    path('list-experts/',views.list_experts),
    path('bulk-remove-experts/',views.bulk_remove_experts),


    path('add-placed-student/',views.PlacedStudentAPIView.as_view()),
    path('view-placed-student/',views.PlacedStudentAPIView.as_view()),
    path('edit-placed-student/<uuid:id>',views.PlacedStudentAPIView.as_view()),
    path('delete-placed-student/<uuid:id>',views.PlacedStudentAPIView.as_view()),
    path('edit-student-testimonials/<int:id>',views.edit_student_testimonials),
    path('delete-student-testimonials/<int:id>',views.delete_student_testimonials),
    path('list-student-testimonials/',views.list_student_testimonials),
    path('bulk-remove-student-testimonials/',views.bulk_remove_student_testimonials),

    path('add-blog/',views.add_blog),
    path('view-blog/',views.view_blog),
    path('view-single-blog/<pk>',views.view_single_blog),
    path('edit-blog/<pk>',views.edit_blog),
    path('delete-blog/<pk>',views.delete_blog),
    path('list-blog/',views.list_blog),
    path('list-recent-blog/',views.list_recent_blog),
    path('list-featured-blog/',views.list_featured_blog),
    path('list-single-blog/<slug:slug>',views.list_single_blog),
    path('search-blog/',views.search_blog),
    path('list-categories/',views.list_categories),
    path('list-tags/',views.list_tags),
    path('list-category-blog/<pk>',views.list_category_blog),
    path('list-tag-blog/<pk>',views.list_tag_blog),

    path('create-comment/<pk>',views.create_comment),
    path('list-comment/<pk>',views.list_comment),

    path('add-career/',views.add_career),
    path('view-career/',views.view_career),
    path('edit-career/<pk>',views.edit_career),
    path('delete-career/<pk>',views.delete_career),
    path('list-career/',views.list_career),
    path('list-hiring/',views.list_hiring),


    path('apply-job/',views.apply_job),
    path('view-apply-job/',views.view_apply_job),
    path('delete-apply-job/<pk>',views.delete_apply_job),

    path('list-checklist/',views.list_checklist),

    # path('test/',views.test),
    

]