
  # or your custom user model

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, LanguageFolder
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import View
import sys, os
import json  
def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        languages = request.POST.getlist('languages[]')

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
            language_objects = LanguageFolder.objects.filter(name__in=languages)
            user_profile.languages.set(language_objects)
            user_profile.save()

            # Generate a token and send a verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            send_verification_email(user, request)  # Ensure this function is defined

            messages.info(request, "Please check your email to complete registration.")
            return redirect('verification_email_sent')  # Replace with your URL name
        except Exception as e:
            messages.error(request, 'Failed to create account. Error: {}'.format(e))

    return render(request, 'create_account.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



###########################################################3333
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Part of your create_account view
def send_verification_email(user, request):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.get_host()
    verification_link = f'http://{domain}{reverse("activate_account", args=[uid, token])}'
    subject = 'Account Verification'
    message = f'Hi {user.username}, please verify your account by clicking on this link: {verification_link}'
    send_mail(subject, message, '142202024@smail.iitpkd.ac.in', [user.email], fail_silently=False)


###############################################################
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

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

    return redirect('some-view')  # Redirect after deletion
##################################################################################


from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to login page after successful activation
        messages.success(request, "Your account has been activated, you can now login.")
        return redirect('loginpage')
    else:
        # Invalid link
        messages.error(request, "Invalid activation link")
        return redirect('Create_account')



######################################################################
# views.py
from django.shortcuts import render

def verification_email_sent(request):
    return render(request, 'verification_email_sent.html')

####################################################################

from django.shortcuts import render, redirect

def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_active=False).first()
        if user:
            send_verification_email(user, request)
            # Show a success message or redirect
            messages.success(request, 'Your e-mail was successfully verified!')
        else:
            messages.success(request, 'your email verification was not successful!, please try again')
    return render(request, 'resend_verification_email.html')




##################################################

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


##################################################################
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect



@login_required
def admin_home_page(request):
    # Check if the user is a superuser or an admin
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        return redirect('some_other_page')
    
    # Fetch all languages
    languages = LanguageFolder.objects.all()

    # Pass both the user and the languages to the template
    return render(request, 'admin_home_page.html', {'user': request.user, 'languages': languages})


########################################################################

def add_remove(request):
    # Your logic here
    return render(request, 'add_remove.html')

from django.http import JsonResponse

def check_language_exists(request):
    language_name = request.POST.get('language_name')
    exists = LanguageFolder.objects.filter(name=language_name).exists()
    return JsonResponse({'exists': exists})




#################################################################################



def assign_task(request):
    # Your logic here
    return render(request, 'assign_task.html')

def check_annotation(request):
    # Your logic here for 'check_annotation' view
    return render(request, 'check_annotation.html')

def start_annotation(request):
    # Your logic here for 'start_annotation' view
    return render(request, 'start_annotation.html')

def download_data_admin(request):
    # Your logic here for 'download_data_admin' view
    return render(request, 'download_data_admin.html')

def api_settings(request):
    # Your logic here for 'api_settings' view
    return render(request, 'api_settings.html')

def settings(request):
    # Your logic here for 'settings' view
    return render(request, 'settings.html')


def verification_email_sent(request):
    return render(request, 'verification_email_sent.html')

from django.views import View
from django.views import View
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
        language, created = LanguageFolder.objects.get_or_create(name=language_name)

        if created:
            return JsonResponse({'message': 'Language added successfully.'})
        else:
            return JsonResponse({'message': 'Language already exists.'})



from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import LanguageFolder

@require_http_methods(["POST"])
# def add_language(request):
#     language_name = request.POST.get('language_name')
#     if not language_name:
#         return JsonResponse({'error': 'The language name is required.'}, status=400)

#     Language.objects.create(name=language_name)
#     return JsonResponse({'status': 'success'})
def add_language(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language_name = data.get('language_name')

        # Check if the language already exists
        if LanguageFolder.objects.filter(name=language_name).exists():
            return JsonResponse({'exists': True, 'message': 'This language already exists.'})

        # Add new language
        LanguageFolder.objects.create(name=language_name)
        return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


from django.shortcuts import render
from .models import Image
from django.shortcuts import render, get_object_or_404
from .models import LanguageFolder 

def language_folder(request, language_name):
    images = Image.objects.filter(language__name=language_name)
    return render(request, 'language_folder.html', {'images': images, 'language_name': language_name})




class RemoveLanguageView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        language_name = data.get('language_name')

        # Perform the deletion operation
        try:
            language = LanguageFolder.objects.get(name=language_name)
            language.delete()
            return JsonResponse({'status': 'success'})
        except LanguageFolder.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Language not found'}, status=404)



from django.views import View
from django.shortcuts import render, redirect
from .models import Image
from .forms import ImageUploadForm

from django.shortcuts import redirect, render
from django.views import View
from .forms import ImageUploadForm
from .models import LanguageFolder, Image

from django.http import JsonResponse

class ImageUploadView(View):
    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            # Instead of 'language_name', we will use 'language_folder_id' to find the right folder
            language_folder_id = request.POST.get('language_folder_id')  # This will be passed from the form
            try:
                language_folder = LanguageFolder.objects.get(id=language_folder_id)
            except LanguageFolder.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Language folder not found"}, status=404)

            image.language_folder = language_folder
            image.save()
            # Return a JSON response with image details
            return JsonResponse({"status": "success", "image": {"id": image.id, "url": image.image.url}})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data"}, status=400)

    
class ImageDeleteView(View):
    def post(self, request, image_id):
        Image.objects.filter(id=image_id).delete()
        return redirect('admin_home_page')

from django.shortcuts import render, redirect
from .models import Image
from django.http import JsonResponse
import json

# Existing views...

from django.http import JsonResponse, HttpResponse
from .models import Image, LanguageFolder

def upload_image(request):
    if request.method == 'POST':
        language_id = request.POST.get('language_id')
        try:
            language = LanguageFolder.objects.get(id=language_id)
        except LanguageFolder.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Language not found"}, status=404)

        image_file = request.FILES.get('image')
        if image_file:
            new_image = Image(language=language, image=image_file)
            new_image.save()
            return JsonResponse({"status": "success", "image_id": new_image.id})
        else:
            return JsonResponse({"status": "error", "message": "Invalid data"})


# views.py
# from django.http import JsonResponse
# from .models import Image, Language

# def get_images_for_language(request, language_name):
#     try:
#         language = Language.objects.get(name=language_name)
#         images = Image.objects.filter(language=language)  # Assuming an Image model with a language field
#         images_data = [{'id': image.id, 'url': image.file.url, 'name': image.name} for image in images]
#         return JsonResponse({'status': 'success', 'images': images_data})
#     except Language.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'Language not found'}, status=404)
# # views.py

from django.shortcuts import render
from .models import Image

def get_images_for_language(request, language_name):
    images = Image.objects.filter(language=language_name)
    return render(request, 'Language_folder.html', {'images': images, 'language_name': language_name})


########## after endsem #########
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Annotation
# from django.http import JsonResponse

# def submit_annotation(request):
#     if request.method == 'POST':
#         # Extract data from request
#         image_name = request.POST.get('imageName')
#         user_text = request.POST.get('userText')

#         # Create and save annotation instance
#         annotation = Annotation(image_name=image_name, user_text=user_text)
#         annotation.save()

#         return JsonResponse({'status': 'success', 'annotation_id': annotation.id})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# def verify_annotation(request, annotation_id):
#     if request.method == 'POST':
#         annotation = get_object_or_404(Annotation, id=annotation_id)
#         action = request.POST.get('action')  # 'approve' or 'reject'

#         if action == 'approve':
#             annotation.status = 'Verified'
#         elif action == 'reject':
#             annotation.status = 'Rejected'
#             annotation.feedback = request.POST.get('feedback', '')

#         annotation.save()
#         return redirect('unverified_annotations')  # Redirect to the list of unverified annotations

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# def get_unverified_annotations(request):
#     unverified_annotations = Annotation.objects.filter(status='Unverified')
#     return render(request, 'admin_verification_page.html', {'annotations': unverified_annotations})
