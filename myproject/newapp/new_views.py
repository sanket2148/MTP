from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Language, Image, Assignment, Annotation
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.views import View
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
import random
from django.db import IntegrityError
from smtplib import SMTPException
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import decorator_from_middleware
from django.contrib.auth import authenticate, login, logout
from .forms import ImageUploadForm
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.decorators.csrf import csrf_exempt



# Helper functions and decorators
def admin_check(user):
    return user.is_authenticated and user.userprofile.user_type == 'admin'

def no_cache(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view_func

no_cache = decorator_from_middleware(CacheMiddleware)

def generate_otp():
    return random.randint(100000, 999999)

# View functions
def send_otp(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        recipient_email = data.get('email')

        if recipient_email:
            otp = generate_otp()
            request.session['otp'] = otp
            try:
                send_mail(
                    'Your OTP for TalkScribe account',
                    f'Here is your OTP: {otp}',
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Failed to send OTP. {str(e)}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        languages = request.POST.getlist('languages[]')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'create_account.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'create_account.html')
        try:
            user = User.objects.create_user(username, email, password)
            user.is_active = False
            user.save()

            user_profile = UserProfile.objects.create(
                user=user,
                user_type=user_type,
            )
            language_objects = Language.objects.filter(name__in=languages)
            user_profile.languages.set(language_objects)
            user_profile.save()

            # Send email with OTP
            otp = generate_otp()
            send_mail(
                'Your OTP for Account Verification',
                f'Your OTP is: {otp}',
                'sanketavaralli321@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            request.session['otp'] = otp
            return redirect('verify_otp', user.id)
        except IntegrityError as e:
            messages.error(request, f'Error creating account: {e}')
        except Exception as e:
            messages.error(request, f'Unexpected error: {e}')
    return render(request, 'create_account.html')

def verify_otp(request, user_id):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if user_otp == session_otp:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect('loginpage')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html')

def delete_user_by_email(request, email):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')  # Replace with your home page

    try:
        user = User.objects.get(email=email)
        user.delete()
        messages.success(request, "User deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('home')


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
            # Log the user in
            login(request, user)

            # Redirect based on user role
            if user_role == 'admin':
                return redirect('admin_home_page')
            elif user_role == 'annotator':
                # Redirect to annotator page (replace 'annotator_page' with the actual view name)
                return redirect('annotator_page')
            elif user_role == 'researcher':
                # Redirect to researcher page (replace 'researcher_page' with the actual view name)
                return redirect('researcher_page')
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid username or password')

    # Render the login page for GET request or if authentication fails
    return render(request, 'loginpage.html')

@login_required
def admin_home_page(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        return redirect('home')
    languages = Language.objects.all()
    return render(request, 'admin_home_page.html', {'languages': languages})

@login_required
@user_passes_test(admin_check)
def add_remove(request):
    return render(request, 'add_remove.html')

@login_required
def check_language_exists(request):
    if request.method == 'POST':
        language_name = request.POST.get('language_name')
        exists = Language.objects.filter(name=language_name).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('loginpage')

@login_required
def assign_task(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        image_id = request.POST.get('image_id')
        try:
            user = User.objects.get(pk=user_id)
            image = Image.objects.get(pk=image_id)
            Assignment.objects.create(image=image, annotator=user, assigned_by=request.user)
            messages.success(request, "Task assigned successfully.")
            return redirect('assignment_list')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
        except Image.DoesNotExist:
            messages.error(request, "Image not found.")
    return render(request, 'assign_task.html')

class RemoveLanguageView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        language_name = data.get('language_name')
        try:
            language = Language.objects.get(name=language_name)
            language.delete()
            return JsonResponse({'status': 'success'})
        except Language.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Language not found'}, status=404)

class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            language_name = request.POST.get('language_name')
            try:
                language = Language.objects.get(name=language_name)
                image.language = language
                image.save()
                return JsonResponse({'status': 'success', 'image_id': image.id})
            except Language.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Language not found'}, status=404)
        return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)

class ImageDeleteView(View):
    def post(self, request, *args, **kwargs):
        image_id = request.POST.get('image_id')
        try:
            image = Image.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'status': 'success'})
        except Image.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)

def get_images_for_language(request, language_name):
    try:
        language = Language.objects.get(name=language_name)
        images = Image.objects.filter(language=language)
        return render(request, 'language_folder.html', {'images': images, 'language': language})
    except Language.DoesNotExist:
        messages.error(request, 'Language not found')
        return redirect('home')

def language_overview(request):
    languages = Language.objects.all()
    language_details = [{
        'name': language.name,
        'images_count': Image.objects.filter(language=language).count(),
        'annotators_count': UserProfile.objects.filter(languages=language, user_type='annotator').count(),
        'annotations_count': Annotation.objects.filter(image__language=language).count()
    } for language in languages]
    return render(request, 'language_overview.html', {'language_details': language_details})

@login_required
def image_list(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist.")
        return redirect('error_page')  # Redirect to an error page

    if user_profile.user_type == 'admin':
        images = Image.objects.filter(uploaded_by=request.user)
    elif user_profile.user_type == 'annotator':
        languages = user_profile.languages.all()
        images = Image.objects.filter(language__in=languages)
    elif user_profile.user_type == 'researcher':
        images = Image.objects.all()
    else:
        messages.error(request, "Invalid user type.")
        return redirect('error_page')  # Redirect to an error page

    return render(request, 'image_list.html', {'images': images})

@login_required
def annotation_list(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile does not exist.")
        return redirect('error_page')  # Redirect to an error page

    if user_profile.user_type == 'researcher':
        annotations = Annotation.objects.all()
    else:
        annotations = Annotation.objects.filter(image__uploaded_by=request.user)

    return render(request, 'annotation_list.html', {'annotations': annotations})

def toggle_dark_mode(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.dark_mode_enabled = not profile.dark_mode_enabled
    profile.save()
    return redirect('settings')

@method_decorator(csrf_exempt, name='dispatch')
class AddLanguageView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        language_name = data.get('language_name')

        if not language_name:
            return JsonResponse({'error': 'Language name is required.'}, status=400)

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

        if Language.objects.filter(name=language_name).exists():
            return JsonResponse({'exists': True, 'message': 'This language already exists.'})

        Language.objects.create(name=language_name)
        return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def upload_image(request):
    if request.method == 'POST':
        language_name = request.POST.get('language_name', None)
        if language_name is None:
            return JsonResponse({'status': 'error'})

        try:
            language = Language.objects.get(name=language_name)
        except Language.DoesNotExist:
            return JsonResponse({'status': 'error'})

        for file in request.FILES.getlist('image'):
            Image.objects.create(language=language, image=file, title=file.name, uploaded_by=request.user)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

# Additional view implementations can be added here
