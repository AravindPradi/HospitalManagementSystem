from django.urls import path
from . import views




urlpatterns = [

    path('',views.home,name='home'),

    path('register_splash',views.register,name='user_register'),

    path('add_dept',views.add_dept,name='add_dept'),

    path('custom_login',views.custom_login,name='custom_login'),

    path('logout',views.logout,name='logout'),

    path('patient-profile',views.patient_profile,name='patient_profile'),

    path('patient-register',views.patient_register,name='patient_register'),

    path('patient_dashboard',views.patient_dashboard,name='patient_dashboard'),

    path('patient-appointment',views.p_appointment,name='p_appointment'),

    path('change-password/', views.reset_password, name='change_password'),



    #doctor pages

    path('doctor-register',views.doc_register,name='doc_register'),

    path('profile',views.profile,name='profile'),

    path('update_profile/', views.update_profile, name='update_profile'),

    path('doctor_dashboard',views.doctor_dashboard,name='doctor_dashboard'),

    path('appointment_done/<int:appointment_id>/', views.appointment_done, name='appointment_done'),

    path('upcomings',views.upcomings,name='upcomings'),

    path('mark_notifications_as_read',views.mark_notifications_as_read,name='mark_notifications_as_read'),
    
    path('notifications',views.notifications,name='notifications'),

    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),

    path('all_patient_details',views.all_patient_details,name='all_patient_details'),

    




    #Admin panel

    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),

    path('doc-details',views.doc_details,name='doc_details'),

    path('doctor-approvals',views.approvals,name='approvals'),

    path('doc-delete/<int:pk>',views.doc_delete,name='doc_delete'),

    path('doc-update-admin/<int:pk>',views.doc_update,name='doc_update'),

    path('all-appointments',views.all_appointments,name='admin_appointments'),

    path('all-departments',views.all_dept,name='all_dept'),

    path('admin_approve/<int:doctor_id>/', views.admin_approve, name='admin_approve'),

    path('admin_reject/<int:doctor_id>/', views.admin_reject, name='admin_reject'),




   
]
