from django.urls import path
from . import views

app_name = 'agency_admin'

urlpatterns = [
    # Staff Portal Routes
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/leads/', views.staff_leads_list, name='staff_leads_list'),
    path('staff/leads/<int:lead_id>/', views.staff_lead_detail, name='staff_lead_detail'),
    path('staff/posts/', views.staff_posts_list, name='staff_posts_list'),
    path('staff/posts/new/', views.staff_post_create, name='staff_post_create'),
    path('staff/posts/<int:post_id>/edit/', views.staff_post_edit, name='staff_post_edit'),
    path('staff/case-studies/new/', views.staff_case_study_create, name='staff_case_study_create'),
    path('staff/case-studies/<int:cs_id>/edit/', views.staff_case_study_edit, name='staff_case_study_edit'),
    path('staff/guides/new/', views.staff_guide_create, name='staff_guide_create'),

    # Custom Superuser Admin Portal Routes
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users_list, name='admin_users_list'),
    path('users/new/', views.admin_user_create, name='admin_user_create'),
    path('users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('users/<int:user_id>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('leads/', views.admin_leads_list, name='admin_leads_list'),
    path('leads/<int:lead_id>/', views.admin_lead_detail, name='admin_lead_detail'),
    path('leads/<int:lead_id>/delete/', views.admin_lead_delete, name='admin_lead_delete'),
    path('leads/export-csv/', views.admin_leads_export_csv, name='admin_leads_export_csv'),
    path('posts/', views.admin_posts_list, name='admin_posts_list'),
    path('posts/<int:post_id>/publish/', views.admin_post_toggle_publish, name='admin_post_toggle_publish'),
    path('posts/<int:post_id>/edit/', views.admin_post_edit, name='admin_post_edit'),
    path('posts/<int:post_id>/delete/', views.admin_post_delete, name='admin_post_delete'),
    path('case-studies/', views.admin_case_studies_list, name='admin_case_studies_list'),
    path('case-studies/new/', views.admin_case_study_create, name='admin_case_study_create'),
    path('case-studies/<int:cs_id>/edit/', views.admin_case_study_edit, name='admin_case_study_edit'),
    path('case-studies/<int:cs_id>/delete/', views.admin_case_study_delete, name='admin_case_study_delete'),
    path('services/', views.admin_services_list, name='admin_services_list'),
    path('services/new/', views.admin_service_create, name='admin_service_create'),
    path('services/<int:service_id>/edit/', views.admin_service_edit, name='admin_service_edit'),
    path('services/<int:service_id>/delete/', views.admin_service_delete, name='admin_service_delete'),
    path('guides/', views.admin_guides_list, name='admin_guides_list'),
    path('guides/new/', views.admin_guide_create, name='admin_guide_create'),
    path('guides/<int:guide_id>/delete/', views.admin_guide_delete, name='admin_guide_delete'),
    path('settings/', views.admin_settings, name='admin_settings'),
    path('pages/', views.admin_pages, name='admin_pages'),
]
