from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<slug:slug>/', views.case_study_detail, name='case_study_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_single, name='blog_single'),
    path('guides/', views.guides, name='guides'),
    path('free-course/', views.free_course, name='free_course'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('partners/', views.partners, name='partners'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]
