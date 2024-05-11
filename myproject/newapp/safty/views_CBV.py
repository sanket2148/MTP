
  # or your custom user model
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import UserProfile, Language
# Include other necessary imports...
from django.core.mail import send_mail
from django.urls import reverse


# Include other necessary imports...


class CreateAccountView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_account.html')

    def post(self, request, *args, **kwargs):
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
            language_objects = Language.objects.filter(name__in=languages)
            user_profile.languages.set(language_objects)
            user_profile.save()

            # Generate a token and send a verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            self.send_verification_email(user, request)

            messages.info(request, "Please check your email to complete registration.")
            return redirect('verification_email_sent')  # Replace with your URL name
        except Exception as e:
            messages.error(request, 'Failed to create account. Error: {}'.format(e))
            return render(request, 'create_account.html')

def send_verification_email(self, user, request):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.get_host()
    verification_link = f'http://{domain}{reverse("activate_account", args=[uid, token])}'
    subject = 'Account Verification'
    message = f'Hi {user.username}, please verify your account by clicking on this link: {verification_link}'
    send_mail(subject, message, '142202024@smail.iitpkd.ac.in', [user.email], fail_silently=False)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



###########################################################3333
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# # Part of your create_account view
# def send_verification_email(user, request):
#     token_generator = PasswordResetTokenGenerator()
#     token = token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     domain = request.get_host()
#     verification_link = f'http://{domain}{reverse("activate_account", args=[uid, token])}'
#     subject = 'Account Verification'
#     message = f'Hi {user.username}, please verify your account by clicking on this link: {verification_link}'
#     send_mail(subject, message, '142202024@smail.iitpkd.ac.in', [user.email], fail_silently=False)


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


from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated, you can now login.")
            return redirect('loginpage')
        else:
            messages.error(request, "Invalid activation link")
            return redirect('create_account')


######################################################################
# views.py
from django.views.generic import TemplateView

class VerificationEmailSentView(TemplateView):
    template_name = 'verification_email_sent.html'

####################################################################

from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# Ensure send_verification_email function is imported

class ResendVerificationEmailView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_active=False).first()
        if user:
            send_verification_email(user, request)
            messages.success(request, 'Your e-mail was successfully verified!')
        else:
            messages.error(request, 'Your email verification was not successful, please try again')
        return redirect('some_page_after_resend')  # Modify as needed

    def get(self, request, *args, **kwargs):
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
from .models import Language
@login_required
def admin_home_page(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        return redirect('some_other_page')

    return render(request, 'admin_home_page.html', {'user': request.user})


########################################################################

def add_remove(request):
    # Your logic here
    return render(request, 'add_remove.html')





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


class CreateAccountView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create_account.html')

    def post(self, request, *args, **kwargs):
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
            language_objects = Language.objects.filter(name__in=languages)
            user_profile.languages.set(language_objects)
            user_profile.save()

            # Generate a token and send a verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            self.send_verification_email(user, request)

            messages.info(request, "Please check your email to complete registration.")
            return redirect('verification_email_sent')  # Replace with your URL name
        except Exception as e:
            messages.error(request, 'Failed to create account. Error: {}'.format(e))
            return render(request, 'create_account.html')

    def send_verification_email(self, user, request):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = request.get_host()
        verification_link = f'http://{domain}{reverse("activate_account", args=[uid, token])}'
        subject = 'Account Verification'
        message = f'Hi {user.username}, please verify your account by clicking on this link: {verification_link}'
        send_mail(subject, message, '142202024@smail.iitpkd.ac.in', [user.email], fail_silently=False)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages



###########################################################3333
# from django.core.mail import send_mail
# from django.urls import reverse
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# # Part of your create_account view
# def send_verification_email(user, request):
#     token_generator = PasswordResetTokenGenerator()
#     token = token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     domain = request.get_host()
#     verification_link = f'http://{domain}{reverse("activate_account", args=[uid, token])}'
#     subject = 'Account Verification'
#     message = f'Hi {user.username}, please verify your account by clicking on this link: {verification_link}'
#     send_mail(subject, message, '142202024@smail.iitpkd.ac.in', [user.email], fail_silently=False)


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


from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.contrib import messages

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated, you can now login.")
            return redirect('loginpage')
        else:
            messages.error(request, "Invalid activation link")
            return redirect('create_account')


######################################################################
# views.py
from django.views.generic import TemplateView

class VerificationEmailSentView(TemplateView):
    template_name = 'verification_email_sent.html'

####################################################################

from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
# Ensure send_verification_email function is imported

class ResendVerificationEmailView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.filter(email=email, is_active=False).first()
        if user:
            send_verification_email(user, request)
            messages.success(request, 'Your e-mail was successfully verified!')
        else:
            messages.error(request, 'Your email verification was not successful, please try again')
        return redirect('some_page_after_resend')  # Modify as needed

    def get(self, request, *args, **kwargs):
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
from .models import Language
@login_required
def admin_home_page(request):
    if not request.user.is_superuser and request.user.userprofile.user_type != 'admin':
        return redirect('some_other_page')

    return render(request, 'admin_home_page.html', {'user': request.user})


########################################################################

def add_remove(request):
    # Your logic here
    return render(request, 'add_remove.html')





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
