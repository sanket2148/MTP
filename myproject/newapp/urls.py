from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import AddLanguageView, RemoveLanguageView #, ImageUploadView, ImageDeleteView
from .views import add_language ,validator ,get_annotations ,assign_annotations
from .views import get_images_for_language ,get_annotation_data_validator,resend_otp , forgot_password
from .views import get_annotators ,settings_validator ,remove_assignment ,language_overview
from .views import save_selected_annotators,unvalidate_annotation ,bulk_assign_annotations,get_unassigned_annotations
from .views import get_selected_annotators, get_assigned_annotators ,get_validators
from .views import save_assignments ,validate_annotation,admin_annotation_validation , delete_account ,change_preferred_language
from . import views
from .views import get_images_from_language ,get_annotations_from_language
from .views import create_annotation , change_password_annotator ,check_annotation_validator,ask_otp
from .views import update_annotation ,request_otp ,verify_reset_password ,change_password_with_old , submit_feedback
from .views import delete_annotation ,update_image_confidentiality,verify_and_reset_password
from .views import annotator , settings_annotator ,download_data_annotator ,start_annotation_annotator, check_annotation_annotator
from .views import delete_selected_images , download_selected_images , language_folder_annotator , get_images_from_language_annotator , get_annotations_from_language_annotator ,get_annotation_data_annotator
from .views import researcher ,check_annotation_researcher ,download_data_researcher ,start_annotation_researcher , settings_researcher, get_annotation_data_researcher #get_all_annotators_for_language , 
urlpatterns = [
    path('', views.welcomepage, name='welcomepage'),
    path('create_account/', views.create_account, name='create_account'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'), 
    
    path('loginpage/', views.loginpage, name='loginpage'),
    path('loginpage/forgot_password/', views.forgot_password, name='forgot_password'),
    path('loginpage/forgot_password/ask_otp/', ask_otp, name='ask_otp'),
    path('loginpage/forgot_password/verify_reset_password/', verify_reset_password, name='verify_reset_password'),
    
    path('admin_home_page/', views.admin_home_page, name='admin_home_page'),
    path('language_overview/', language_overview, name='language_overview'),
    path('admin_home_page/add_remove/', views.add_remove, name='add_remove'),
    path('admin_home_page/assign_task/', views.assign_task, name='assign_task'),
    path('admin_home_page/check_annotation/', views.check_annotation, name='check_annotation'),
    path('admin_home_page/start_annotation/', views.start_annotation, name='start_annotation'),
    path('admin_home_page/download_data_admin/', views.download_data_admin, name='download_data_admin'),
    path('admin_home_page/api_settings/', views.api_settings, name='api_settings'),
    path('admin_home_page/settings/', views.settings, name='settings'),
    path('admin_home_page/settings/change_password', views.change_password, name='change_password'),
    path('admin_home_page/settings/help', views.help, name='help'),
    path('admin_annotation_validation/', views.admin_annotation_validation, name='admin_annotation_validation'),

    path('annotator/settings/change_password_annotator', views.change_password_annotator, name='change_password_annotator'),
    path('annotator/settings/help', views.help, name='help'),
    path('researcher/settings/change_password_researcher', views.change_password_researcher, name='change_password_researcher'),
    path('researcher/settings/help', views.help, name='help'),
    path('help', views.help, name='help'),
    
    #path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('verification-email-sent/', views.verification_email_sent, name='verification_email_sent'),
    path('delete-user/<str:email>/', views.delete_user_by_email, name='delete_user_by_email'),
    path('login/', views.login_view, name='login'),
    #path('template/loginpage/', views.loginpage, name='loginpage'),
    # ... existing URLs ...
    path('add_language/', views.AddLanguageView.as_view(), name='add_language'),
    path('remove_language/', views.RemoveLanguageView.as_view(), name='remove_language'),
    path('upload_image/', views.upload_image, name='upload_image'),
    #path('delete_image/', ImageDeleteView.as_view(), name='delete_image'),
    # path('get_images/<str:language_name>/', get_images_for_language, name='get_images_for_language'),
    path('admin_home_page/language_folder/<str:language_name>/', views.language_folder, name='language_folder'),
    path('delete_selected_images/', delete_selected_images, name='delete_selected_images'),
    path('download_selected_images/', download_selected_images, name='download_selected_images'),
    #path('images/<str:language_name>/', views.get_images_for_language, name='get_images_for_language'),

    ######after endsem
    path('update_image_confidentiality/', update_image_confidentiality, name='update_image_confidentiality'),

    path('logout/', views.logout_view, name='logout'),
    path('get_language_data/<str:language_name>/', views.get_language_data, name='get_language_data'),
    
    
    ##########   ADD_REMOVE ############
    path('get_annotators/<str:language>', views.get_annotators, name='get_annotators'),
    path('save_selected_annotators/', views.save_selected_annotators, name='save_selected_annotators'),
    path('get_assigned_annotators/<str:language>/', views.get_assigned_annotators, name='get_assigned_annotators'),
    
    #####################  ASSIGN_TASK ##########
    path('get_selected_annotators/<str:language>/', views.get_selected_annotators, name='get_selected_annotators'),
    path('get_images_for_language/<str:language>/', views.get_images_for_language, name='get_images_for_language'),
    path('is_image_assigned/', views.is_image_assigned, name='is_image_assigned'),
    path('save_assignments/', save_assignments, name='save_assignments'),
    path('get_assigned_images/<str:annotator>/', views.get_assigned_images, name='get_assigned_images'),
    path('remove_assignment/', remove_assignment, name='remove_assignment'),
    path('get_assigned_images/<str:annotator>/<str:language_name>/', views.get_assigned_images, name='get_assigned_images'),
    #############################Start_annotation##########
    path('get_images_from_language/', get_images_from_language, name='get_images_from_language'),
    path('get_annotations_from_language/', get_annotations_from_language, name='get_annotations_from_language/'),
    path('create_annotation/', create_annotation, name='create_annotation'),
    path('update_annotation/', update_annotation, name='update_annotation'),
    path('newapp/delete_annotation/', delete_annotation, name='delete_annotation'),
    
    
    #####################Check Annotation ###############
    path('get_annotation_data/<str:language>/', views.get_annotation_data, name='get_annotation_data'),
    path('validate_annotation/', views.validate_annotation, name='validate_annotation'),
    path('unvalidate_annotation/', views.unvalidate_annotation, name='unvalidate_annotation'),
    
    path('get_validators/<str:language_name>/', views.get_validators, name='get_validators'),
    path('get_annotations/<str:language>/', views.get_annotations, name='get_annotations'),
    path('assign_annotations/', views.assign_annotations, name='assign_annotations'),
    path('get_unassigned_annotations/<int:validator_id>/<int:number_of_annotations>/', get_unassigned_annotations, name='get_unassigned_annotations'),
    path('bulk_assign_annotations/', bulk_assign_annotations, name='bulk_assign_annotations'),
    ########################################################
    ################      Annotator_homepage ################
    path('annotator/', views.annotator, name='annotator'),
    path('annotator/check_annotation_annotator', views.check_annotation_annotator, name='check_annotation_annotator'),
    path('annotator/start_annotation_annotator', views.start_annotation_annotator, name='start_annotation_annotator'),
    path('annotator/download_data_annotator', views.download_data_annotator, name='download_data_annotator'),
    path('annotator/settings_annotator', views.settings_annotator, name='settings_annotator'),          
    path('annotator/language_folder_annotator/<str:language_name>/', views.language_folder_annotator, name='language_folder_annotator'),
    path('get_images_from_language_annotator/', get_images_from_language_annotator, name='get_images_from_language_annotator'),
    path('get_annotations_from_language_annotator/', get_annotations_from_language_annotator, name='get_annotations_from_language_annotator'),
    path('get_annotation_data_annotator/<str:language_name>/', get_annotation_data_annotator, name='get_annotation_data_annotator'),
    #####################################################
    ################### Researcher_Homepage  #############
    path('researcher/', views.researcher, name='researcher'),
    path('reseacher/check_annotation_researcher/', views.check_annotation_researcher, name='check_annotation_researcher'),
    path('researcher/start_annotation_researcher/', views.start_annotation_researcher, name='start_annotation_researcher'),
    path('researcher/download_data_researcher/', views.download_data_researcher, name='download_data_researcher'),
    path('researcher/settings_researcher', views.settings_researcher, name='settings_researcher'),          
    path('annotator/language_folder_researcher/<str:language_name>/', views.language_folder_researcher, name='language_folder_researcher'),
    
    # path('get_all_annotators_for_language/', views.get_all_annotators_for_language, name='get_all_annotators_for_language'),
    # path('newapp/get_all_annotators_for_language/', views.get_all_annotators_for_language, name='get_all_annotators_for_language'),
    path('get_annotation_data_researcher/<str:language_name>/', get_annotation_data_researcher, name='get_annotation_data_researcher'),
    ###################### Setting of all users ############################################
    path('verify_reset_password/', verify_and_reset_password, name='verify_reset_password'),
    path('request_otp/', request_otp, name='request_otp'),
    path('change_password_with_old/', change_password_with_old, name='change_password_with_old'),
    path('delete_account/', delete_account, name='delete_account'),
    path('submit_feedback/',submit_feedback, name="submit_feedback"),
    path('change_preferred_language/', change_preferred_language, name='change_preferred_language'),
    
    
    ################################### validator ########################3
    path('validator/', views.validator, name='validator'),
    path('check_annotation_validator/', views.check_annotation_validator, name='check_annotation_validator'),
    path('settings_validator/', views.settings_validator, name='settings_validator'),
    path('get_annotation_data_validator/<str:language_name>/', views.get_annotation_data_validator, name='get_annotation_data_validator'),
    
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
