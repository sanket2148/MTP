# or your custom user model
from smtplib import SMTPException
from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .forms import ImageUploadForm
from .models import Annotation, Image, Language, UserProfile, SelectedAnnotators
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
import sys, os
import json
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware
from django.core.mail import send_mail
import random
from django.contrib.auth import logout
from .models import Image
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from .models import Assignment
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.conf import settings


def admin_check(user):
    return user.is_authenticated and user.userprofile.user_type == 'admin'

def welcomepage(request):
    return render(request, 'welcomepage.html')

def no_cache(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view_func

# Use decorator_from_middleware if you want to convert middleware to a decorator
no_cache = decorator_from_middleware(CacheMiddleware)
# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)
# def send_otp(request):
#     if request.method == 'POST' and request.is_ajax():
#         data = json.loads(request.body)
#         recipient_email = data.get('email')
        
#         if recipient_email:
#             otp = generate_otp()
#             request.session['otp'] = otp

#             try:
#                 # Send the OTP to the recipient's email
#                 send_mail(
#                     'Your OTP for TalkScribe account',
#                     f'Here is your OTP: {otp}',
#                     settings.EMAIL_HOST_USER,  # Sender's email
#                     [recipient_email],  # Recipient's email
#                     fail_silently=False,
#                 )
#                 return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})
#             except Exception as e:
#                 return JsonResponse({'status': 'error', 'message': f'Failed to send OTP. {str(e)}'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Email is required.'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Language
import random
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import random

from django.db import models
from django.utils import timezone
import datetime

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Assuming OTP is valid for 5 minutes
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=5)

def create_account(request):
    if request.method == 'POST':
        temp_user_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'user_type': request.POST.get('user_type'),
            'selected_languages': request.POST.getlist('languages'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
        }
        
        # Generate and store the OTP in session
        otp = random.randint(100000, 999999)
        request.session['otp'] = str(otp)  # Convert to string for consistency
        request.session['temp_user_data'] = temp_user_data

        # Send OTP via email
        subject = 'Your OTP for account verification'
        message = f"Dear {temp_user_data['first_name']},\n\nThank you for choosing Talk-Scribe. We're excited to have you join our family!\n\nYour username is: {temp_user_data['username']}\nYour OTP for account verification is: {otp}\n\nPlease click on the link below to verify your account and get started:\nhttp://yourdomain.com/verification_page\n\nThank you,\nThe Talk-Scribe Team"
        send_mail(subject, message, 'sanketavralli321@gmail.com', [temp_user_data['email']], fail_silently=False)
        
        messages.info(request, 'Please check your email for the OTP to verify your account.')
        return redirect('verify_otp')  # Redirect to OTP verification page

    else:
        # Logic to display the account creation form
        return render(request, 'create_account.html')




import time

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Language

from django.contrib.auth.models import User
from .models import UserProfile, Language

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp', '')
        
        if user_otp == session_otp:
            # OTP is verified, proceed to create user and profile from session data
            temp_user_data = request.session.pop('temp_user_data', None)
            if temp_user_data:
                user = User.objects.create_user(
                    username=temp_user_data['username'],
                    email=temp_user_data['email'],
                    password=temp_user_data['password']
                )
                user.first_name = temp_user_data['first_name']
                user.last_name = temp_user_data['last_name']
                user.save()

                # Create UserProfile
                user_profile = UserProfile(user=user, user_type=temp_user_data['user_type'])
                user_profile.save()

                # Associate selected languages with UserProfile
                if temp_user_data['user_type'] in ['annotator', 'validator']:
                    selected_languages = Language.objects.filter(id__in=temp_user_data['selected_languages'])
                    user_profile.languages.set(selected_languages)

                messages.success(request, 'Account verified and created successfully.')
                return redirect('loginpage')  # Or wherever you want to redirect after creation
            else:
                messages.error(request, 'Verification failed. Please try again.')
                return redirect('create_account')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html')
    else:
        return render(request, 'verify_otp.html')




from django.http import JsonResponse

def resend_otp(request):
    if request.method == 'POST' and 'temp_user_data' in request.session:
        temp_user_data = request.session['temp_user_data']
        # Generate a new OTP
        new_otp = random.randint(100000, 999999)
        request.session['otp'] = new_otp  # Update session with new OTP
        
        # Resend the OTP via email
        subject = 'Your new OTP'
        message = f'Your new OTP is: {new_otp}'
        send_mail(subject, message, 'sanketavaralli321@gmail.com', [temp_user_data['email']], fail_silently=False)
        
        return JsonResponse({'status': 'success', 'message': 'OTP resent successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Could not resend OTP.'}, status=400)






def delete_user_by_email(request, email):
    if not request.user.is_superuser:  # Optional: restrict this function to admin users
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('some-view')  # Redirect to a safe page

    try:
        user = User.objects.get(email=email)
        user.delete()
        messages.success(request, "User deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('create_account')  # Redirect after deletion

from .models import OTPModel
def loginpage(request):
    if request.method == 'POST':
        # Extract information from form
        user_role = request.POST.get('user_role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_password = 'remember_password' in request.POST

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user's selected role matches their actual role
            if user.userprofile.user_type == user_role:
                # Log the user in
                login(request, user)

                # Redirect based on user role
                if user_role == 'admin' or user.is_superuser:
                    return redirect('admin_home_page')
                elif user_role == 'annotator':
                    # Redirect to annotator page (replace 'annotator_page' with the actual view name)
                    return redirect('annotator')
                elif user_role == 'researcher':
                    # Redirect to researcher page (replace 'researcher_page' with the actual view name)
                    return redirect('researcher')
                elif user_role == 'validator':
                    # Redirect to researcher page (replace 'researcher_page' with the actual view name)
                    return redirect('validator')
            else:
                # Display an error message if the selected role doesn't match the user's actual role
                messages.error(request, 'Invalid user role selected. Please try again.')
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid username or password')

    # Render the login page for GET request or if authentication fails
    return render(request, 'loginpage.html')



def forgot_password(request):
    # Your logic here
    return render(request, 'forgot_password.html')

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


@csrf_exempt
@require_http_methods(["POST"])
def ask_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'success': False, 'error': 'Email address is required.'}, status=400)

        # Generate and store OTP
        otp = generate_otp()  # Implement this function to generate OTP
        
        # Print the OTP to the terminal for debugging
        print(f"Generated OTP for {email}: {otp}")
        
        OTPModel.objects.create(email=email, otp=otp)

        # Send email with OTP
        send_mail(
            'Your OTP',
            f'Your OTP is: {otp}',
            'sanketavaralli321@gmail.com',  # Update this
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error: {e}")
    return JsonResponse({'success': True})


# def generate_otp():
#     # Implement OTP generation logic here
#     # For simplicity, you might return a fixed value or use a library like PyOTP
#     return '123456'  # Example OTP, replace with actual generation logic
# At the top of your views.py (or wherever you're using OTPModel)


@csrf_exempt
@require_http_methods(["POST"])
def verify_reset_password(request):
    data = json.loads(request.body)
    print("Received data:", data)  # Debug print
    otp = data.get('otp')
    new_password = data.get('newPassword')
    email = data.get('email')

    if not all([otp, new_password, email]):
        return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)

    # Verify OTP
    try:
        otp_record = OTPModel.objects.get(email=email, otp=otp)
        # Optionally, check if OTP is expired based on your logic
    except OTPModel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid or expired OTP.'}, status=400)

    # Reset password
    try:
        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()

        # Optionally, invalidate the OTP after successful password reset
        otp_record.delete()

        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    
##################################################################


def login_view(request):
    if request.method == 'POST':
        credential = request.POST.get('username')  # This can be either username or email
        password = request.POST.get('password')

        # First, try to authenticate assuming 'credential' is a username
        user = authenticate(username=credential, password=password)

        if user is None:
            # If authentication fails, try to fetch the user by email
            try:
                user_obj = User.objects.get(email=credential)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None and user.is_active:
            login(request, user)
            # Redirect to a specific page based on user role or a default page
            return redirect('some_home_page')  # Replace with your specific redirect logic
        else:
            messages.error(request, 'Invalid username/email or password')

    return render(request, 'loginpage.html')
#########################################################################




@login_required
def admin_home_page(request):
    # Check if the user is a superuser or an admin
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        messages.error(request, 'Username does not belong to an admin')
        return redirect('loginpage')
    
    # Fetch all languages
    languages = Language.objects.all()

    # Aggregate data by language for images uploaded by the logged-in user
    language_details = Image.objects.filter(uploaded_by=request.user).values(
        'language__name'
    ).annotate(
        images_count=Count('id', distinct=True),
        # Count annotations across all images uploaded by the user, by any annotator
        annotations_count=Count('annotation', distinct=True),
        # Count distinct annotators for all images uploaded by the user
        annotators_count=Count('annotation__annotator', distinct=True)
    ).order_by('language__name')

    # Pass both the languages and language_details to the template
    context = {
        'user': request.user, 
        'languages': languages, 
        'language_details': language_details
    }
    return render(request, 'admin_home_page.html', context)


########################################################################
@login_required
@user_passes_test(admin_check)
def add_remove(request):
    # Your logic here
    return render(request, 'add_remove.html')



@login_required
def check_language_exists(request):
    language_name = request.POST.get('language_name')
    exists = Language.objects.filter(name=language_name).exists()
    return JsonResponse({'exists': exists})



@login_required
def logout_view(request):
    logout(request)
    return redirect('loginpage')  # Redirect to login URL

#################################################################################


# @login_required
# def assign_task(request):
#     # Your logic here
#     return render(request, 'assign_task.html')
@login_required
def check_annotation(request):
    # Your logic here for 'check_annotation' view
    return render(request, 'check_annotation.html')
@login_required
def start_annotation(request):
    # Your logic here for 'start_annotation' view
    return render(request, 'start_annotation.html')
@login_required
def download_data_admin(request):
    # Your logic here for 'download_data_admin' view
    return render(request, 'download_data_admin.html')
@login_required
def api_settings(request):
    # Your logic here for 'api_settings' view
    return render(request, 'api_settings.html')
@login_required
def settings(request):
    # Your logic here for 'settings' view
    return render(request, 'settings.html')

@login_required
def verification_email_sent(request):
    return render(request, 'verification_email_sent.html')

def toggle_dark_mode(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.dark_mode_enabled = not profile.dark_mode_enabled
    profile.save()
    return redirect('settings') 



@method_decorator(csrf_exempt, name='dispatch')
class AddLanguageView(View):
    def post(self, request, *args, **kwargs):
        # Assuming the language name is sent in JSON format
        data = json.loads(request.body)
        language_name = data.get('language_name')

        if not language_name:
            # Handle the case where language_name is not provided
            return JsonResponse({'error': 'Language name is required.'}, status=400)

        # Create the new Language object
        language, created = Language.objects.get_or_create(name=language_name)

        if created:
            return JsonResponse({'message': 'Language added successfully.'})
        else:
            return JsonResponse({'message': 'Language already exists.'})




@require_http_methods(["POST"])
def add_language(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language_name = data.get('language_name')

        # Check if the language already exists
        if Language.objects.filter(name=language_name).exists():
            return JsonResponse({'exists': True, 'message': 'This language already exists.'})

        # Add new language
        Language.objects.create(name=language_name)
        return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

#################################################################################
#####   Language_folder

from django.contrib.auth.decorators import user_passes_test
def has_view_all_languages_permission(user):
    return user.has_perm('newapp.view_all_languages') or user.userprofile.user_type in ['Annotator', 'Researcher']

# @user_passes_test(has_view_all_languages_permission)
@login_required
def language_folder(request, language_name):
    language = Language.objects.get(name=language_name)
    images = Image.objects.filter(language=language, uploaded_by=request.user)

    return render(request, 'language_folder.html', {'images': images, 'language_name': language_name})







from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.text import slugify
@login_required
def upload_image(request):
    if request.method == 'POST':
        language_name = request.POST.get('language_name', None)
        if not language_name:
            messages.error(request, 'Language name is missing.')
            return JsonResponse({'status': 'error', 'message': 'Language name is missing.'})

        try:
            language = Language.objects.get(name=language_name)
        except Language.DoesNotExist:
            messages.error(request, 'Specified language does not exist.')
            return JsonResponse({'status': 'error', 'message': 'Specified language does not exist.'})

        images_uploaded = 0
        duplicate_images = 0
        for file in request.FILES.getlist('image'):
            original_name = file.name
            base, extension = original_name.rsplit('.', 1) if '.' in original_name else (original_name, '')
            new_name = f"{slugify(base)}_{request.user.id}.{extension}" if extension else slugify(base)
            if Image.objects.filter(title=new_name, language=language).exists():
                duplicate_images += 1
                continue  # Skip this file as it's a duplicate

            try:
                # Rename the file
                file.name = new_name
                # Now you can create a new Image instance with the renamed file
                Image.objects.create(language=language, image=file, title=new_name, uploaded_by=request.user)
                images_uploaded += 1
            except (ValidationError, IntegrityError) as e:
                messages.error(request, f"Error uploading image {file.name}: {e}")
                continue  # Skip this file due to an error

        if images_uploaded:
            messages.success(request, f'{images_uploaded} images uploaded successfully.')
        if duplicate_images:
            messages.warning(request, f'{duplicate_images} duplicate images were not uploaded.')

        return JsonResponse({
            'status': 'success',
            'message': f'{images_uploaded} images uploaded, {duplicate_images} duplicates skipped.'
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



from django.http import HttpResponse
from zipfile import ZipFile
from io import BytesIO

import io
import zipfile
from django.http import HttpResponse
from django.core.files.base import ContentFile
import io
import zipfile
from django.http import HttpResponse
from django.core.files.base import ContentFile

import io
import zipfile
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

import json

import io
import zipfile
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Image  # Import your Image model here
@login_required
def download_selected_images(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        
        # Extract the selected image IDs from the JSON data
        selected_image_ids = data.get('selectedImageIds', [])
        
        print("selected_image_ids:", selected_image_ids)
        
        # Fetch images from the database based on selected_image_ids
        images = Image.objects.filter(id__in=selected_image_ids)

        # Create a zip file containing selected images
        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(in_memory_zip, mode='w') as zipf:
            for image in images:
                # Read the image data from the image_file field
                image_data = image.image.read()
                
                # Write the image data to the zip file with a unique name
                zipf.writestr(f'{image.title}.jpg', image_data)

        # Create a Django HttpResponse with the zip file
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="selected_images.zip"'
        in_memory_zip.seek(0)
        response.write(in_memory_zip.read())

        return response
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")





@login_required
def delete_selected_images(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        
        # Extract the selected image IDs from the JSON data
        selected_image_ids = data.get('selectedImageIds', [])
        
        print("selected_image_ids:", selected_image_ids)
        
        try:
            # Delete images from the database based on selected_image_ids
            Image.objects.filter(id__in=selected_image_ids).delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("Error deleting images:", str(e))
            return JsonResponse({'status': 'error', 'message': 'An error occurred while deleting images.'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=400)



###############################################################################

@login_required
def image_list(request):
    # Ensure the user has a UserProfile
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist.")
        return redirect('error_page')  # Redirect to an error page or wherever is appropriate

    # Filter images based on the user type
    if user_profile.user_type == 'admin':
        images = Image.objects.filter(uploaded_by=request.user)
    elif user_profile.user_type == 'annotator':
        languages = user_profile.languages.all()
        images = Image.objects.filter(language__in=languages)
    elif user_profile.user_type == 'researcher':
        images = Image.objects.all()
    else:
        messages.error(request, "Invalid user type.")
        return redirect('error_page')  # Redirect to an error page or wherever is appropriate

    return render(request, 'image_list.html', {'images': images})


########################################################################################3


@login_required
def annotation_list(request):
    # Ensure the user has a UserProfile
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist.")
        return redirect('error_page')  # Redirect to an error page or wherever is appropriate

    # Filter annotations based on the user type
    if user_profile.user_type == 'researcher':
        annotations = Annotation.objects.all()
    else:
        # Ensure that the Image model has 'uploaded_by' field as a ForeignKey to User
        annotations = Annotation.objects.filter(image__uploaded_by=request.user)

    return render(request, 'annotation_list.html', {'annotations': annotations})


########################################################################################



@login_required
def assign_task(request):
    # Check if the user is an admin
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('error_page')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')  # Changed from annotator_id
        image_id = request.POST.get('image_id')

        try:
            user = User.objects.get(pk=user_id)
            if user.userprofile.user_type != 'annotator':
                raise ValueError("Selected user is not an annotator")
            image = Image.objects.get(pk=image_id)
        except (User.DoesNotExist, Image.DoesNotExist, ValueError) as e:
            messages.error(request, str(e))
            return redirect('error_page')

        Assignment.objects.create(image=image, annotator=user, assigned_by=request.user)
        messages.success(request, "Task assigned successfully.")
        return redirect('assignment_list')

    return render(request, 'assign_task.html')


#############################################################################################################


class RemoveLanguageView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        language_name = data.get('language_name')

        # Perform the deletion operation
        try:
            language = Language.objects.get(name=language_name)
            language.delete()
            return JsonResponse({'status': 'success'})
        except Language.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Language not found'}, status=404)







class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)  # Debugging: print POST data
        print(request.FILES)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            language_name = request.POST.get('language_name')  # Get language_name instead of id
            try:
                language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Language folder not found"}, status=404)

            image.language = language  # Assuming Image model has a 'language' ForeignKey to Language
            image.save()
            
            # Assuming you want to return all images of this language
            images = Image.objects.filter(language=language)
            image_list = [{"id": img.id, "url": img.image.url} for img in images]

            return JsonResponse({"status": "success", "images": image_list})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data"}, status=400)
    
class ImageDeleteView(View):
    def post(self, request, image_id):
        Image.objects.filter(id=image_id).delete()
        return redirect('admin_home_page')



# def get_images_for_language(request, language_name):
#     images = Image.objects.filter(language=language_name)
#     return render(request, 'Language_folder.html', {'images': images, 'language_name': language_name})




from django.shortcuts import render
from .models import Language, Image, Annotation
from django.contrib.auth.decorators import login_required

from django.db.models import Count

@login_required
def language_overview(request):
    user = request.user
    uploaded_images = Image.objects.filter(uploaded_by=user).select_related('language')
    
    # Aggregate data by language
    languages = uploaded_images.values('language__name').annotate(
        images_count=Count('id'),
        annotations_count=Count('annotation'),
        annotators_count=Count('annotation__annotator', distinct=True)
    )
    
    context = {'language_details': languages}
    return render(request, 'admin_home_page.html', context)








##################################################################################






def get_language_data(request, language_name):
    try:
        language = Language.objects.get(name=language_name)
        images = Image.objects.filter(language=language).values('id', 'title', 'image')

        images_data = [{
            'id': img['id'],
            'title': img['title'],
            'url': request.build_absolute_uri(settings.MEDIA_URL + str(img['image']))
        } for img in images]

        return JsonResponse({'images': images_data})

    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)



# Function-based view
@login_required
def settings(request):
    # Your view logic here
    languages = Language.objects.all()
    return render(request, 'settings.html', {'languages': languages})  # Render the appropriate template









##################################################################################################################



# In your_app/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Image  # Ensure this is the correct import path for your Image model
from django.views.decorators.csrf import csrf_exempt

@require_http_methods(["POST"])
@login_required
  # Only use csrf_exempt if you cannot send the CSRF token. Otherwise, it's better to include it for security.
def update_image_confidentiality(request):
    try:
        data = json.loads(request.body)
        image_ids = data.get('image_ids')
        is_confidential = data.get('is_confidential', False)

        # Filter images by ID and ensure they belong to the logged-in user if necessary
        images = Image.objects.filter(id__in=image_ids)  # Add more filters as needed

        # Update the confidentiality setting for the filtered images
        for image in images:
            image.is_confidential = is_confidential
            image.save()

        return JsonResponse({'status': 'success', 'message': 'Confidentiality updated successfully.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Error updating confidentiality.'}, status=500)






#ADD _REMOVE ############


def get_annotators(request, language):
    try:
        # Get the Language object based on the name
        language_obj = Language.objects.get(name__iexact=language)

        # Filter annotators based on language
        annotators = User.objects.filter(userprofile__user_type='annotator', userprofile__languages=language_obj)

        # If no annotators found
        if not annotators:
            return JsonResponse({'message': 'No annotators available for this language'}, status=200)

        # Convert annotators to a list of dictionaries
        annotators_data = [{'username': annotator.username, 'id': annotator.id} for annotator in annotators]

        # Return JSON response
        return JsonResponse(annotators_data, safe=False)

    except ObjectDoesNotExist:
        # Handle case where the language does not exist
        return JsonResponse({'message': 'Language not found'}, status=404)



from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import SelectedAnnotators, Language  # Adjust the import path based on your project structure
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
import json

from .models import User, Language, SelectedAnnotators

@csrf_exempt
@login_required
def save_selected_annotators(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user = request.user
    selected_annotators_list = data.get('selected_annotators')

    errors = []

    try:
        with transaction.atomic():
            # Process each item in the list if the list is not empty
            if selected_annotators_list:
                for annotator_info in selected_annotators_list:
                    username = annotator_info.get('username')
                    language_name = annotator_info.get('language')

                    try:
                        language = Language.objects.get(name=language_name)
                        annotator_user = User.objects.get(username=username)

                        # Get or create the SelectedAnnotators instance
                        selected_annotator, _ = SelectedAnnotators.objects.get_or_create(user=user, language=language)

                        # Add or retain the annotator
                        selected_annotator.annotators.add(annotator_user)

                    except Language.DoesNotExist:
                        errors.append({'username': username, 'language': language_name, 'error': 'Language does not exist'})
                    except User.DoesNotExist:
                        errors.append({'username': username, 'language': language_name, 'error': 'User does not exist'})
                    except Exception as e:
                        errors.append({'username': username, 'language': language_name, 'error': str(e)})

            # Remove unselected annotators for each language
            for language in Language.objects.all():
                selected_annotator_qs = SelectedAnnotators.objects.filter(user=user, language=language)
                if selected_annotator_qs.exists():
                    selected_annotator = selected_annotator_qs.first()
                    current_annotators = set(selected_annotator.annotators.all())
                    annotators_to_keep = set(User.objects.filter(username__in=[ai['username'] for ai in selected_annotators_list if ai['language'] == language.name]))

                    annotators_to_remove = current_annotators - annotators_to_keep
                    for annotator in annotators_to_remove:
                        selected_annotator.annotators.remove(annotator)

    except IntegrityError as e:
        return JsonResponse({'error': 'Database error occurred', 'details': str(e)}, status=500)

    if errors:
        return JsonResponse({'message': 'Some annotators could not be updated', 'errors': errors}, status=400)

    return JsonResponse({'message': 'Annotators updated successfully'}, status=200)







from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import SelectedAnnotators, Language

@login_required
def get_assigned_annotators(request, language):
    user = request.user
    language_obj = get_object_or_404(Language, name=language)

    selected_annotators_instances = SelectedAnnotators.objects.filter(user=user, language=language_obj)

    assigned_annotators = []
    for selected_annotator_instance in selected_annotators_instances:
        assigned_annotators.extend(selected_annotator_instance.annotators.all())

    annotator_usernames = [annotator.username for annotator in assigned_annotators]

    return JsonResponse({'selected_annotators': annotator_usernames})



from django.contrib.auth.models import User

def getLanguageForAnnotator(annotator_username):
    try:
        annotator = User.objects.get(username=annotator_username)
        selected_annotator = SelectedAnnotators.objects.get(annotators=annotator)
        languages = selected_annotator.languages.all()
        
        # Assuming each annotator is associated with only one language
        if languages:
            return languages[0].name
        else:
            print(f"No languages found for annotator {annotator_username}.")
            return None
    except User.DoesNotExist:
        print(f"User with username {annotator_username} not found.")
        return None
    except SelectedAnnotators.DoesNotExist:
        print(f"SelectedAnnotators entry not found for annotator {annotator_username}.")
        return None




##########################################################################################################

#########  Assign_TASK ############


from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Language  # Import the Language model from your models module

def get_selected_annotators(request, language):
    try:
        language_obj = Language.objects.get(name=language)
        selected_annotators = SelectedAnnotators.objects.filter(language=language_obj, user=request.user)

        annotators_list = [{'username': annotator.username} for selection in selected_annotators
                           for annotator in selection.annotators.all()]

        if annotators_list:
            return JsonResponse({'annotators': annotators_list}, status=200)
        else:
            return JsonResponse({'annotators': []}, status=200)

    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language does not exist'}, status=404)
    except ObjectDoesNotExist:
        return JsonResponse({'annotators': []}, status=200)  # No annotators found, return an empty list
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from .models import Image, Annotation

def get_images_for_language(request, language):
    # Get the images filtered by language and the user who uploaded them
    images = Image.objects.filter(language__name=language, uploaded_by=request.user)

    # Prepare a subquery to check if an annotation exists for each image
    annotations_subquery = Annotation.objects.filter(image=OuterRef('pk'))

    # Annotate each image object with a boolean indicating if it's annotated
    images = images.annotate(
        is_annotated=Exists(annotations_subquery)
    )

    # Create a list of dictionaries, each representing an image with its annotation status
    image_list = [
        {
            'title': image.title,
            'filename': image.image.name,
            'is_annotated': image.is_annotated
        } for image in images
    ]

    # Return the data as JSON
    return JsonResponse({'images': image_list})

# def get_images_for_language(request, language):
#     # language = Language.objects.get(pk=language)
#     images = Image.objects.filter(language=language).annotate(
#         is_annotated=Exists(Annotation.objects.filter(image=OuterRef('pk')))
#     ).values('title', 'filename', 'is_annotated')  # Adjust fields as necessary

#     return JsonResponse({"images": list(images)})


# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Assignment, Language, Image
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Language, Assignment, Image
import json

from django.db.models import Q

@login_required
def save_assignments(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    selected_language = data.get('language')
    assigned_images = data.get('assignedImages')

    if not selected_language or not assigned_images:
        return JsonResponse({'error': 'Incomplete data provided'}, status=400)

    user = request.user

    try:
        language = Language.objects.get(name=selected_language)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language does not exist'}, status=400)

    try:
        with transaction.atomic():
            # Remove existing assignments not present in the received data
            existing_assignments = Assignment.objects.filter(language=language, assigned_by=user)
            for assignment in existing_assignments:
                annotator = assignment.annotator.username
                if annotator not in assigned_images or assignment.image.title not in assigned_images[annotator]:
                    assignment.delete()

            # Save new assignments
            for annotator, images in assigned_images.items():
                annotator_user = User.objects.get(username=annotator)
                for title in images:
                    try:
                        image = Image.objects.get(title=title, language=language)
                        # Check if the assignment already exists
                        existing_assignment = Assignment.objects.filter(
                            image=image,
                            language=language,
                            annotator=annotator_user,
                            assigned_by=user
                        ).exists()
                        if not existing_assignment:
                            assignment = Assignment.objects.create(
                                image=image,
                                language=language,
                                annotator=annotator_user,
                                assigned_by=user,
                                status='Assigned'
                            )
                            image.status = 'Assigned'
                            image.save()
                    except Image.DoesNotExist:
                        print(f"Image with title {title} does not exist for the given language")
                        continue

        return JsonResponse({'success': True})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': f'Error saving assignments: {str(e)}'}, status=500)







def is_image_assigned(request):
    image_id = request.GET.get('image_id')
    annotator_id = request.GET.get('annotator_id')
    assigned = Assignment.objects.filter(image_id=image_id, annotator__id=annotator_id).exists()
    return JsonResponse({'assigned': assigned})


# views.py

# views.py

# views.py

@login_required
def get_assigned_images(request, annotator):
    try:
        # Get the logged-in user
        logged_in_user = request.user
        
        # Query the Assignment model to get assigned images for the annotator assigned by the logged-in user
        assignments = Assignment.objects.filter(annotator__username=annotator, assigned_by=logged_in_user)
        
        # Extract image titles from the assignments
        assigned_images = [assignment.image.title for assignment in assignments]
        print("Fetched images:", assigned_images)
        # Return the assigned image titles in the response
        return JsonResponse({'images': assigned_images})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def remove_assignment(request):
    # Extract data from the request body
    data = json.loads(request.body)
    annotator = data.get('annotator')
    image_title = data.get('imageTitle')

    # Check if annotator and image_title are provided
    if not annotator or not image_title:
        return JsonResponse({'error': 'Incomplete data provided'}, status=400)

    # Query the Assignment model to find the assignment to be removed
    try:
        assignment = Assignment.objects.get(annotator__username=annotator, image__title=image_title)
    except Assignment.DoesNotExist:
        return JsonResponse({'error': 'Assignment does not exist'}, status=404)

    # Delete the assignment
    assignment.delete()

    return JsonResponse({'success': True})



###############################################################################
#### start_annotation


# views.py
# #from django.http import JsonResponse
# from .models import Image, Language

# def get_images_from_language(request):
#     language_name = request.GET.get('language')
#     try:
#         language = Language.objects.get(name=language_name)
#         images = Image.objects.filter(language=language).values('id', 'title', 'image')
#         images_data = list(images)
#         return JsonResponse({'images': images_data}, safe=False)
#     except Language.DoesNotExist:
#         return JsonResponse({'error': 'Language not found'}, status=404)
    
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Image, Language

@login_required
def get_images_from_language(request):
    language_name = request.GET.get('language')
    try:
        # Ensure you're also considering the 'created_by' filter for the language if applicable
        language = Language.objects.get(name=language_name)
        # Filter images by language and the uploaded_by field for the current user
        images = Image.objects.filter(language=language, uploaded_by=request.user).values('id', 'title', 'image', 'created_at')
        images_data = list(images)
        return JsonResponse({'images': images_data}, safe=False)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

        
        
        
        
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Annotation, Language

@login_required
def get_annotations_from_language(request):
    language_name = request.GET.get('language')
    try:
        language = Language.objects.get(name=language_name)
        annotations = Annotation.objects.filter(language=language, annotator=request.user).values(
            'id', 'image__title', 'annotation', 'created_at'
        )
        annotations_data = list(annotations)
        return JsonResponse({'annotations': annotations_data}, safe=False)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

        
        
        
        

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Image, Annotation, Language
from django.views.decorators.csrf import csrf_exempt  # For demonstration purposes only
from django.core.exceptions import ValidationError
@csrf_exempt  # Note: It's better to use CSRF token properly in production

@require_POST
def create_annotation(request):
    image_id = request.POST.get('image_id')
    annotation_text = request.POST.get('annotation')
    language_name = request.POST.get('language')

    try:
        image = Image.objects.get(pk=image_id)
        language = Language.objects.get(name=language_name)
        annotation = Annotation(image=image, annotation=annotation_text, language=language, annotator=request.user)
        annotation.save()

        return JsonResponse({'success': True, 'annotationId': annotation.id})  # Return the ID of the new annotation
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
@require_POST
def update_annotation(request):
    try:
        data = json.loads(request.body)
        annotation_id = data.get('annotationId')
        new_text = data.get('newText')

        annotation = Annotation.objects.get(pk=annotation_id)
        annotation.annotation = new_text
        annotation.save()

        # After updating the annotation, recalculate similarity and update validation status
        # annotation.calculate_and_update_similarity()

        return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Annotation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
 # Make sure this import is correct

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Annotation

@require_POST
def delete_annotation(request):
    try:
        data = json.loads(request.body)
        annotation_id = data.get('annotationId')

        if not annotation_id:
            return JsonResponse({'error': 'Missing annotation ID'}, status=400)

        Annotation.objects.get(pk=annotation_id).delete()
        return JsonResponse({'success': True})
    except Annotation.DoesNotExist:
        return JsonResponse({'error': 'Annotation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
################################################
###############  Check Annotation Admin ######################

from django.http import JsonResponse
from .models import SelectedAnnotators
from django.contrib.auth.decorators import login_required

@login_required
def get_annotators_for_language(request):
    language_name = request.GET.get('language', None)
    if language_name:
        selected_annotators = SelectedAnnotators.objects.filter(
            user=request.user,
            language__name=language_name
        ).first()
        
        annotators_list = []
        if selected_annotators:
            annotators = selected_annotators.annotators.all()
            annotators_list = [{'id': annotator.id, 'username': annotator.username} for annotator in annotators]
        
        return JsonResponse({'annotators': annotators_list})
    return JsonResponse({'error': 'No language selected'}, status=400)


@login_required
def get_annotations_by_annotator(request, annotator_id):
    images = Image.objects.filter(uploaded_by=request.user, annotation__annotator_id=annotator_id).distinct()
    annotations_data = []
    for image in images:
        annotations = Annotation.objects.filter(image=image, annotator_id=annotator_id)
        annotations_list = [{'id': annotation.id, 'text': annotation.annotation} for annotation in annotations]
        annotations_data.append({
            'image_id': image.id,
            'image_title': image.title,
            'annotations': annotations_list
        })
    
    return JsonResponse({'data': annotations_data})





# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import SelectedAnnotators, Annotation, Image

from django.http import JsonResponse
from .models import Annotation, Image, SelectedAnnotators

from django.contrib.auth.models import User

def get_annotation_data(request, language):
    user = request.user
    selected_annotators = SelectedAnnotators.objects.filter(user=user, language__name=language).first()

    if not selected_annotators:
        return JsonResponse({'error': 'Selected annotators not found'}, status=404)

    annotators_list = [annotator.username for annotator in selected_annotators.annotators.all()]

    images_uploaded_by_user = Image.objects.filter(uploaded_by=user, language=selected_annotators.language)
    annotation_data = {}

    # Include logged-in user's annotations
    annotation_data[user.username] = []
    annotations_by_user = Annotation.objects.filter(annotator=user, language=selected_annotators.language, image__in=images_uploaded_by_user)
    for annotation in annotations_by_user:
        annotation_data[user.username].append({
            'id': annotation.id,
            'image': annotation.image.id,
            'img': annotation.image.image.url,
            'annotator': annotation.annotator.id,
            'annotation': annotation.annotation,
            'created_at': annotation.created_at,
            'validated': annotation.validated,
            'validated_by': annotation.validated_by.id if annotation.validated_by else None
        })

    for annotator in annotators_list:
        if annotator != user.username:  # Skip the logged-in user, as we've already included their annotations
            annotation_data[annotator] = []
            # Fetch annotations only for images uploaded by the logged-in user
            annotations = Annotation.objects.filter(annotator__username=annotator, language=selected_annotators.language, image__in=images_uploaded_by_user)
            for annotation in annotations:
                annotation_data[annotator].append({
                    'id': annotation.id,
                    'image': annotation.image.id,
                    'img': annotation.image.image.url,
                    'annotator': annotation.annotator.id,
                    'annotation': annotation.annotation,
                    'created_at': annotation.created_at,
                    'validated': annotation.validated,
                    'validated_by': annotation.validated_by.id if annotation.validated_by else None
                })

    result = {
        'annotators': annotators_list,
        'images': [image.image.url for image in images_uploaded_by_user],
        'data': annotation_data,
    }

    return JsonResponse(result)




# views.py
from django.shortcuts import render


@login_required
def validator(request):
    # Check if the user is a superuser or an admin
    if not request.user.is_superuser and request.user.userprofile.user_type != 'validator':
        messages.error(request, 'username not belongs to Validator')
        return redirect('loginpage')
    
    # Fetch all languages
    languages = Language.objects.all()

    # Pass both the user and the languages to the template
    return render(request, 'validator.html', {'user': request.user, 'languages': languages})

from django.http import JsonResponse

@login_required
def admin_annotation_validation(request):
    # Check if the user is a superuser or an admin
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        messages.error(request, 'username not belongs to admin')
        return redirect('loginpage')
    
    # Fetch all languages
    languages = Language.objects.all()

    # Pass both the user and the languages to the template
    return render(request, 'admin_annotation_validation.html', {'user': request.user, 'languages': languages})
from django.http import JsonResponse
from .models import Annotation

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Annotation

from django.http import JsonResponse
from .models import Annotation, ValidationTask
@csrf_exempt
@login_required
def validate_annotation(request):
    if request.method == 'POST':
        # Get data from the request
        annotation_id = request.POST.get('annotation_id')
        validated_by_id = request.POST.get('validated_by_id')

        # Check if annotation_id and validated_by_id are valid integers
        try:
            annotation_id = int(annotation_id)
            validated_by_id = int(validated_by_id)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid annotation or validator ID'})

        try:
            annotation = Annotation.objects.get(id=annotation_id)

            # Check if the user performing the validation is an admin
            validated_by = User.objects.get(id=validated_by_id)
            if not validated_by.is_superuser:
                return JsonResponse({'success': False, 'error': 'Only admins can validate annotations'})

            annotation.validated = True
            annotation.validated_by_id = validated_by_id
            annotation.save()

            # Update ValidationTask status
            validation_task = ValidationTask.objects.filter(annotation=annotation).first()
            if validation_task:
                validation_task.status = 'Validated'
                validation_task.save()

            return JsonResponse({'success': True})
        except Annotation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Annotation does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
@csrf_exempt
@login_required
def unvalidate_annotation(request):
    if request.method == 'POST':
        # Get annotation ID from the POST data
        annotation_id = request.POST.get('annotation_id')

        # Check if annotation_id is a valid integer
        try:
            annotation_id = int(annotation_id)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid annotation ID'})

        try:
            # Retrieve the annotation object
            annotation = Annotation.objects.get(pk=annotation_id)

            # Check if the user performing the unvalidation is an admin
            unvalidated_by = request.user
            if not unvalidated_by.is_superuser:
                return JsonResponse({'success': False, 'error': 'Only admins can unvalidate annotations'})

            # Update the validated field to False
            annotation.validated = False
            annotation.save()

            # Update ValidationTask status
            validation_task = ValidationTask.objects.filter(annotation=annotation).first()
            if validation_task:
                validation_task.status = 'Assigned'  # Update to the appropriate status
                validation_task.save()

            return JsonResponse({'success': True})
        except Annotation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Annotation does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})






@login_required
def get_validators(request, language_name):
    # Check if the language exists
    language = get_object_or_404(Language, name=language_name)
    
    # Filter validators based on language
    validators = UserProfile.objects.filter(user_type='validator', languages__name__icontains=language_name)

    # Check if validators were found
    if validators.exists():
        validators_data = [{'id': validator.user.id, 'username': validator.user.username} for validator in validators]
        return JsonResponse({'validators': validators_data})
    else:
        return JsonResponse({'validators': []})

@login_required
def get_annotations(request, language):
    selected_language = get_object_or_404(Language, name=language)

    # Fetch annotations for the selected language with related image and annotator information
    annotations = Annotation.objects.filter(
        language=selected_language,
        image__uploaded_by=request.user
    ).select_related('image', 'annotator')

    annotations_list = []

    for annotation in annotations:
        # Check if the annotation has been assigned
        assigned = ValidationTask.objects.filter(annotation=annotation).exists()

        # Check if the annotation has been validated
        validated = ValidationTask.objects.filter(annotation=annotation, status='Validated').exists()

        annotations_list.append({
            'id': annotation.id,
            'text': annotation.annotation,
            'image': {
                'id': annotation.image.id,
                'title': annotation.image.title,
                'url': request.build_absolute_uri(annotation.image.image.url),
            },
            'annotator': {
                'id': annotation.annotator.id,
                'username': annotation.annotator.username,
            },
            'assigned': assigned,
            'validated': validated,
        })
    print(annotations_list)
    return JsonResponse({'annotations': annotations_list})



import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Annotation, ValidationTask

from django.db import IntegrityError

@login_required
def assign_annotations(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Extract validator_id and annotation_ids from the JSON data
            validator_id = data.get('validator_id')
            annotation_ids = data.get('annotation_ids', [])
            status = data.get('status', 'Assigned')  # Default to 'Assigned' if not provided

            # Fetch the validator and annotations
            validator = get_object_or_404(User, id=validator_id)
            annotations = Annotation.objects.filter(id__in=annotation_ids)

            # Assign annotations to the validator
            for annotation in annotations:
                # Check if a task already exists for this assignment
                existing_task = ValidationTask.objects.filter(
                    annotation=annotation,
                    validator=validator,
                    assigned_by=request.user,
                ).first()

                if existing_task:
                    # If a task already exists, update its status
                    existing_task.status = status
                    existing_task.save()
                else:
                    # If no task exists, create a new one
                    validation_task = ValidationTask(
                        annotation=annotation,
                        validator=validator,
                        language=annotation.language,
                        image=annotation.image,
                        assigned_by=request.user,
                        status=status,
                    )
                    validation_task.save()

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'Assignment already exists for the selected annotation'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.db import IntegrityError

@login_required
def bulk_assign_annotations(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Extract validator_id and annotation_ids from the JSON data
            validator_id = data.get('validatorId')
            annotation_ids = data.get('annotations', [])
            print(f'Validator ID: {validator_id}')

            # Fetch the validator
            try:
                validator = User.objects.get(id=validator_id)
            except User.DoesNotExist:
                return JsonResponse({'error': f'User with ID {validator_id} does not exist'}, status=404)

            # Fetch the annotations
            annotations = Annotation.objects.filter(id__in=annotation_ids)

            # Assign annotations to the validator
            for annotation in annotations:
                # Check if a task already exists for this assignment
                existing_task = ValidationTask.objects.filter(
                    annotation=annotation,
                    validator=validator,
                    assigned_by=request.user,
                ).first()

                if existing_task:
                    # If a task already exists, update its status
                    existing_task.status = 'Assigned'
                    existing_task.save()
                else:
                    # If no task exists, create a new one
                    validation_task = ValidationTask(
                        annotation=annotation,
                        validator=validator,
                        language=annotation.language,
                        image=annotation.image,
                        assigned_by=request.user,
                        status='Assigned',
                    )
                    validation_task.save()

            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON data: {str(e)}'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'Assignment already exists for the selected annotation'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




import random
@login_required
def get_unassigned_annotations(request, validator_id, number_of_annotations):
    try:
        # Convert validator_id and number_of_annotations to integers
        validator_id = int(validator_id)
        number_of_annotations = int(number_of_annotations)

        # Get the validator object
        validator = get_object_or_404(User, id=validator_id)

        # Get a list of annotation IDs assigned to the validator
        assigned_annotation_ids = ValidationTask.objects.filter(
            validator=validator
        ).values_list('annotation_id', flat=True)

        # Get all unassigned annotation IDs
        all_unassigned_ids = Annotation.objects.exclude(
            id__in=assigned_annotation_ids
        ).values_list('id', flat=True)

        # Randomly select a subset of unassigned IDs
        selected_unassigned_ids = random.sample(list(all_unassigned_ids), min(number_of_annotations, len(all_unassigned_ids)))

        # Fetch the corresponding annotations
        unassigned_annotations = Annotation.objects.filter(id__in=selected_unassigned_ids)

        # Prepare data for JSON response
        data = {'unassignedAnnotations': []}

        for annotation in unassigned_annotations:
            data['unassignedAnnotations'].append({
                'id': annotation.id,
                'annotation': annotation.annotation,
                'image_url': annotation.image.image.url,

                # Add other required attributes
            })

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
####################################################################################################################################
####################################################################################################################################
################################                                                          ##########################################
################################                      Annotator_homepage                  ##########################################
################################                                                          ##########################################
####################################################################################################################################
####################################################################################################################################


from django.shortcuts import render
@login_required
def annotator(request):
    # Check if the user is a superuser or an admin
    if not request.user.is_superuser and request.user.userprofile.user_type != 'annotator':
        return redirect('some_other_page')
    
    # Fetch all languages
    languages = Language.objects.all()
    # Your view logic here
    #return render(request,'')
    return render(request, 'annotator.html', {'user': request.user, 'languages': languages})



###########################
##### check_annotation_annoatator

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Annotation, Image, Language, UserProfile
from django.contrib.auth.decorators import login_required

def check_annotation_annotator(request):
    # Your view logic here
    return render(request,'check_annotation_annotator.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Language, Annotation, Image  # Ensure you have the correct import paths

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Language, Annotation, Image  # Make sure you have the correct import paths


# Only the annotations made by the logged-in user for the specified language are fetched.
# The Annotation.objects.filter() query is updated to filter annotations based on the logged-in user.
# The response includes annotations and images data specific to the logged-in user only.
@login_required
def get_annotation_data_annotator(request, language_name):
    try:
        # Fetch the language object
        language = Language.objects.get(name=language_name)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

    # Fetch annotations made by the logged-in user in the specified language
    annotations_by_user = Annotation.objects.filter(
        annotator=request.user,
        language=language
    ).select_related('image')

    # Prepare annotations data
    annotations_data = [
        {'img': annotation.image.image.url, 'annotation': annotation.annotation}
        for annotation in annotations_by_user
    ]

    # Prepare images data
    images_data = [annotation['img'] for annotation in annotations_data]

    result = {
        'annotators': [request.user.username],
        'data': {
            request.user.username: annotations_data  # Use username as the key
        },
        'images': list(set(images_data))  # Ensure unique images
    }

    return JsonResponse(result)





@login_required
def get_annotators_annotation_data(request):
    return render(request, 'get_annotators_annotation_data')



@login_required
def download_data_annotator(request):
    # Your view logic here
    return render(request,'download_data_annotator.html')

@login_required
def settings_annotator(request):
    # Your view logic here
    languages = Language.objects.all()
    return render(request,'settings_annotator.html', {'languages': languages})





from django.shortcuts import get_object_or_404

@login_required
def language_folder_annotator(request, language_name):
    language = get_object_or_404(Language, name=language_name)
    
    # Assuming the current user is an annotator
    annotator = request.user
    
    # Get assignments for the annotator for the given language
    assignments = Assignment.objects.filter(annotator=annotator, language=language)
    
    # Extract image IDs from assignments
    image_ids = assignments.values_list('image__id', flat=True)
    
    # Get images based on the extracted IDs
    images = Image.objects.filter(id__in=image_ids)
    
    return render(request, 'language_folder_annotator.html', {'images': images, 'language_name': language_name})



##############
################ Startannotation annotator 
@login_required
def start_annotation_annotator(request):
    # Your view logic here
    return render(request,'start_annotation_annotator.html')

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Language, Image, Assignment  # Ensure you have the correct import paths

@login_required
def get_images_from_language_annotator(request):
    language_name = request.GET.get('language')
    try:
        language = Language.objects.get(name=language_name)
        
        assigned_images = Assignment.objects.filter(
            annotator=request.user,
            language=language
        ).select_related('image').values(
            'image__id', 'image__title', 'image__image', 'image__created_at'
        )

        images_data = []
        for img in assigned_images:
            annotation_status = Annotation.objects.filter(image_id=img['image__id']).exists()
            images_data.append({
                'id': img['image__id'],
                'title': img['image__title'],
                'image': img['image__image'],
                'created_at': img['image__created_at'],
                'annotated': annotation_status  # Add annotation status to the image data
            })
        
        return JsonResponse({'images': images_data}, safe=False)
    
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)


    
    
@login_required
def get_annotations_from_language_annotator(request):
    language_name = request.GET.get('language')
    try:
        language = Language.objects.get(name=language_name)
        annotations = Annotation.objects.filter(language=language, annotator=request.user).values(
            'id', 'image__title', 'annotation', 'created_at'
        )
        annotations_data = list(annotations)
        return JsonResponse({'annotations': annotations_data}, safe=False)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)


####################################################################################################################################
####################################################################################################################################
################################                                                          ##########################################
################################                      Researcher_homepage                  ##########################################
################################                                                          ##########################################
####################################################################################################################################
####################################################################################################################################



@login_required
def researcher(request):
    # Your view logic here
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    
    # Fetch all languages
    languages = Language.objects.all()
    
    return render(request,'researcher.html', {'user': request.user, 'languages': languages})
@login_required
def language_folder_researcher(request, language_name):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    language = Language.objects.get(name=language_name)
    images = Image.objects.filter(language=language,is_confidential=False)

    return render(request, 'language_folder_researcher.html', {'images': images, 'language_name': language_name})

@login_required
def check_annotation_researcher(request):   
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page') 
    # Your view logic here
    return render(request,'check_annotation_researcher.html')



@login_required
def start_annotation_researcher(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    # Your view logic here
    return render(request,'start_annotation_researcher.html')


@login_required
def download_data_researcher(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    # Your view logic here
    return render(request,'download_data_researcher.html')

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Annotation, Image, Language, UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def get_annotation_data_researcher(request, language_name):
    try:
        # Fetch the language object
        language = Language.objects.get(name=language_name)
    except Language.DoesNotExist:
        return JsonResponse({'error': 'Language not found'}, status=404)

    # Fetch users (annotators) who have 'annotator' user_type and are associated with the specified language
    annotators = User.objects.filter(userprofile__user_type='annotator', userprofile__languages=language)

    # Prepare annotators list
    annotators_list = [annotator.username for annotator in annotators]

    # Fetch images uploaded by the user that are in the specified language
    images_uploaded_by_user = Image.objects.filter( language=language)
    
    # Prepare annotation data
    annotation_data = {}
    for annotator in annotators:
        annotations = Annotation.objects.filter(annotator=annotator, language=language)
        annotation_data[annotator.username] = [
            {'img': annotation.image.image.url, 'annotation': annotation.annotation}
            for annotation in annotations
        ]

    result = {
        'annotators': annotators_list,
        'images': [image.image.url for image in images_uploaded_by_user],
        'data': annotation_data,
    }

    return JsonResponse(result)









####################################################################################################################################
####################################################################################################################################
################################                                                          ##########################################
################################                      Validator                           ##########################################
################################                                                          ##########################################
####################################################################################################################################
####################################################################################################################################
from django.http import JsonResponse
from .models import Annotation, Image, User, ValidationTask



@login_required
def get_annotation_data_validator(request, language_name):
    # Get the logged-in validator user
    validator = request.user
    language = Language.objects.get(name=language_name)
    # Fetch all validation tasks assigned to the logged-in validator user
    validation_tasks = ValidationTask.objects.filter(validator=request.user, language=language)

    # Initialize data dictionary
    annotation_data = {}
    unique_annotators = set()
    unique_images = set()
    # If no validation tasks are found
    if not validation_tasks:
        result = {
            'annotators': [],
            'images': [],
            'data': annotation_data,
        }
        return JsonResponse(result)

    # Loop through each validation task
    for task in validation_tasks:
        # Get the annotation related to the task
        annotation = task.annotation

        # Get the annotator who annotated the annotation
        annotator = annotation.annotator

        # Get the related image connected to the annotation
        image = annotation.image
        unique_annotators.add(annotator.username)
        # Add image URL to set
        unique_images.add(image.image.url)
        images_list = list(unique_images)
        # Populate annotation data
        annotation_data.setdefault(annotator.username, []).append({
            'id': annotation.id,
            'image': image.id,
            'img': image.image.url,
            'annotator': annotator.id,
            'annotation': annotation.annotation,
            'created_at': annotation.created_at,
            'validated': annotation.validated,
            'validated_by': annotation.validated_by.id if annotation.validated_by else None
        })
    annotators_list = list(unique_annotators)

    # Return the JSON response with the annotation data
    result = {
        'annotators': annotators_list,
        'images': images_list,
        'data': annotation_data,
    }
    return JsonResponse(result)

@login_required
def check_annotation_validator(request):
    # Your view logic here
    return render(request,'check_annotation_validator.html')


@login_required
def settings_validator(request):
    # Your view logic here
    languages = Language.objects.all()
    return render(request,'settings_validator.html', )


####################################################################################################################################
####################################################################################################################################
################################                                                          ##########################################
################################                      Settings of users                   ##########################################
################################                                                          ##########################################
####################################################################################################################################
####################################################################################################################################
@login_required
def settings_researcher(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    # Your view logic here
        languages = Language.objects.all()
    return render(request,'settings_researcher.html')
@login_required
def change_password(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        return redirect('some_other_page')
    # Your view logic here
    return render(request,'change_password.html')
@login_required
def change_password_annotator(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'annotator':
        return redirect('some_other_page')
    # Your view logic here
    return render(request,'change_password_annotator.html')
@login_required
def change_password_researcher(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'researcher':
        return redirect('some_other_page')
    # Your view logic here
    return render(request,'change_password_researcher.html')

def help(request):
    # Your view logic here
    return render(request,'help.html')







from django.contrib.auth.models import User
from django.http import JsonResponse
# Import other necessary modules

def request_otp(request):
    email = request.GET.get('email')
    otp = random.randint(100000, 999999)
    # Store the OTP in the session or database associated with the user's email
    request.session['otp'] = otp  # Example: storing OTP in session
    print(f"Sending OTP to {email}")
    # Send email with OTP
    send_mail(
        'Your OTP for Password Reset',
        f'Your OTP is: {otp}',
        'sanketavaralli321@gmail.com',
        [email],
        fail_silently=False,
    )
    return JsonResponse({'message': 'OTP sent successfully.'})
    # Proceed with OTP generation and sending logic as before

def verify_and_reset_password(request):
    data = json.loads(request.body)
    email = data['email']
    otp = data['otp']
    new_password = data['newPassword']
    
    if request.session.get('otp') == int(otp):
        # Reset Password
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password reset successfully.'})
    else:
        return JsonResponse({'message': 'Invalid OTP'}, status=400)
    # Proceed with OTP verification and password reset logic as before

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

@login_required
def change_password_with_old(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')
        
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
            return JsonResponse({'message': 'Password changed successfully.', 'status': 'success'})
        else:
            return JsonResponse({'message': 'Old password is incorrect.', 'status': 'error'}, status=400)

# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from .models import Annotation, Language
# from django.contrib.auth.decorators import login_required

# @login_required
# def get_all_annotators_for_language(request):
#     language_name = request.GET.get('language', None)
#     if language_name:
#         try:
#             language = Language.objects.get(name=language_name)
#             # Get all annotations in this language
#             annotations = Annotation.objects.filter(language=language).distinct()
#             # Get distinct annotators from those annotations
#             annotators_ids = annotations.values_list('annotator', flat=True).distinct()
#             annotators = User.objects.filter(id__in=annotators_ids)
            
#             annotators_list = [{'id': annotator.id, 'username': annotator.username} for annotator in annotators]
#             return JsonResponse({'annotators': annotators_list})
#         except Language.DoesNotExist:
#             return JsonResponse({'error': 'Language does not exist'}, status=404)
    
#     return JsonResponse({'error': 'No language selected'}, status=400)
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import JsonResponse

from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib import messages
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.core.mail import send_mail
import random

@login_required
def delete_account(request):
    if request.method == 'POST':
        if 'request_otp' in request.POST:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=403)

            # Verify user has an email address
            if not user.email:
                return JsonResponse({'success': False, 'error': 'No email address associated with this account.'}, status=400)
            
            # Generate and send OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)
            request.session['otp_user_id'] = user.id

            subject = 'Account Deletion OTP Verification'
            message = f'Hello {user.first_name},\n\n'\
                      'You have requested to delete your account. '\
                      f'Your OTP for account deletion is: {otp}\n\n'\
                      'If you did not request this, please ignore this email or secure your account.'
            
            try:
                send_mail(
                    subject,
                    message,
                    'sanketavaralli321@gmail.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
                print(f"Sending OTP to {user.email}")  # Added for debugging
                return JsonResponse({'success': True, 'message': 'OTP sent. Please check your email.'})
            except Exception as e:
                print(f"Failed to send OTP email to {user.email}: {e}")  # Added for debugging
                return JsonResponse({'success': False, 'error': f'Failed to send OTP email. {e}'}, status=500)

        elif request.POST.get('confirmation_phrase', '').strip() == 'DELETE MY ACCOUNT':
            # Process account deletion
            user_otp = request.POST.get('otp', '').strip()
            session_otp = request.session.get('otp', '')
            user = request.user
            
            if not user.is_authenticated:
                return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=403)

            if user_otp == session_otp and request.session.get('otp_user_id', None) == user.id:
                logout(request)
                # Perform deletion of related data here
                user.delete()
                # Clear the session after successful deletion
                request.session.pop('otp', None)
                request.session.pop('otp_user_id', None)
                return JsonResponse({'success': True, 'message': 'Your account has been successfully deleted.'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP. Please try again.'}, status=400)
        else:
            # Incorrect confirmation phrase or missing parameters
            return JsonResponse({'success': False, 'error': 'Confirmation phrase is incorrect or missing parameters.'}, status=400)
    else:
        # This action should be accessed via POST only
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)






from django.http import JsonResponse
from .models import Language, UserProfile

def change_preferred_language(request):
    if request.method == 'POST' and request.is_ajax():
        language_id = request.POST.get('language_id')
        try:
            language = Language.objects.get(id=language_id)
            user_profile = request.user.userprofile
            user_profile.preferred_language = language
            user_profile.save()
            return JsonResponse({'success': True})
        except Language.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Selected language does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method or not an AJAX request.'})


from django.http import JsonResponse
from .models import UserFeedback
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use this decorator with caution and consider CSRF protection
def submit_feedback(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        feedback = UserFeedback(
            user=user,
            ui_rating=data.get('ui-rating'),
            ui_feedback=data.get('ui-feedback'),
            image_upload_rating=data.get('image-upload-rating', None),
            image_upload_feedback=data.get('image-upload-feedback', ''),
            annotation_process_rating=data.get('annotation-process-rating'),
            annotation_process_feedback=data.get('annotation-process-feedback'),
            validation_process_rating=data.get('validation-process-rating', None),
            validation_process_feedback=data.get('validation-process-feedback', ''),
            overall_software_rating=data.get('overall-software-rating'),
            overall_feedback=data.get('overall-feedback'),
        )
        feedback.save()
        return JsonResponse({'success': True, 'message': 'Feedback submitted successfully.'})

    # Handle non-POST requests here
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Language
from django.contrib.auth.decorators import login_required

@require_POST
@login_required
@csrf_exempt
def change_preferred_language(request):
    try:
        data = json.loads(request.body)
        language_ids = data.get('language_ids', [])
        languages = Language.objects.filter(id__in=language_ids)
        
        request.user.userprofile.languages.set(languages)
        request.user.userprofile.save()
        
        return JsonResponse({"success": True, "message": "Language preferences updated successfully."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)
