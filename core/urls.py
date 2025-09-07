from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('reporter-dashboard/', views.reporter_dashboard, name='reporter_dashboard'),
    path('editor-dashboard/', views.editor_dashboard, name='editor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('employment-ad-editor/', views.employment_ad_editor, name='employment_ad_editor'),
    path('employment-ad-preview/', views.employment_ad_preview, name='employment_ad_preview'),
    path('employment-ad-preview-embed/', views.employment_ad_preview_embed, name='employment_ad_preview_embed'),
    path('employment-ad-design/', views.employment_ad_design, name='employment_ad_design'),
    path('download-design-pdf/', views.download_design_pdf, name='download_design_pdf'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('update-currency-rates/', views.update_currency_rates_view, name='update_currency_rates'),
    path('test-form-submission/', views.test_form_submission, name='test_form_submission'),
    path('simple-position-submission/', views.simple_position_submission, name='simple_position_submission'),
]
