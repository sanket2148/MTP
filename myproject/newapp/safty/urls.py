from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import AddLanguageView, RemoveLanguageView, ImageUploadView, ImageDeleteView
from .views import add_language
from .views import get_images_for_language


urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('admin_home_page/', views.admin_home_page, name='admin_home_page'),\
    path('admin_home_page/add_remove/', views.add_remove, name='add_remove'),
    path('admin_home_page/assign_task/', views.assign_task, name='assign_task'),
    path('admin_home_page/check_annotation/', views.check_annotation, name='check_annotation'),
    path('admin_home_page/start_annotation/', views.start_annotation, name='start_annotation'),
    path('admin_home_page/download_data_admin/', views.download_data_admin, name='download_data_admin'),
    path('admin_home_page/api_settings/', views.api_settings, name='api_settings'),
    path('admin_home_page/settings/', views.settings, name='settings'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('verification-email-sent/', views.verification_email_sent, name='verification_email_sent'),
    path('delete-user/<str:email>/', views.delete_user_by_email, name='delete_user_by_email'),
    path('login/', views.login_view, name='login'),
    #path('template/loginpage/', views.loginpage, name='loginpage'),
    # ... existing URLs ...
    path('add_language/', views.AddLanguageView.as_view(), name='add_language'),
    path('remove_language/', views.RemoveLanguageView.as_view(), name='remove_language'),
    
    path('delete_image/', ImageDeleteView.as_view(), name='delete_image'),
    path('get_images/<str:language_name>/', get_images_for_language, name='get_images_for_language'),
    path('admin_home_page/language_folder/<str:language_name>/', views.language_folder, name='language_folder'),
    path('upload_image/', ImageUploadView.as_view(), name='upload_image'),
    #path('images/<str:language_name>/', views.get_images_for_language, name='get_images_for_language'),

    ######after endsem
    #path('process_image/', views.process_image, name='process_image'),
    # path('submit_annotation/', views.submit_annotation, name='submit_annotation'),
    # path('verify_annotation/<int:annotation_id>/', views.verify_annotation, name='verify_annotation'),
    # path('unverified_annotations/', views.get_unverified_annotations, name='unverified_annotations'),
    


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)