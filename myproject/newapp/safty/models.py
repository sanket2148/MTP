

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

#from myproject.newapp.views import language_folder 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    #languages = models.ManyToManyField('Language')

    def __str__(self):
        return self.user.username
    



class LanguageFolder(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user_profile = models.ForeignKey(UserProfile, related_name='language_folders',
    on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username}'s {self.name} folder"
    
        
# class Image(models.Model):
#     image_id = models.CharField(max_length=50, primary_key=True)
#     image_name = models.CharField(max_length=100)
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)  # Assuming 'language' is a ForeignKey
#     image = models.ImageField(upload_to="images/", null=True)    

#     def __str__(self):
#         return self.image_name
class Image(models.Model):
    image_name = models.CharField(max_length=100)
    language_folder = models.ForeignKey(LanguageFolder, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.image_name
    
class Annotator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    languages = models.ManyToManyField(LanguageFolder)  # Assuming a Language model exists

    def __str__(self):
        return self.user.username


class Annotation(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    annotation_id = models.CharField(max_length=50, primary_key=True)
    annotation_text = models.TextField()  # Renamed from 'annotation' for clarity
    annotator = models.ForeignKey(Annotator, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=20, default='Unverified')  # Added from second model
    # feedback = models.TextField(null=True, blank=True)  # Added from second model

    def __str__(self):
        return self.annotation_id



class Download(models.Model):
    download_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    download_type = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    annotations = models.ManyToManyField(Annotation, blank=True)
    num_annotations_downloaded = models.IntegerField(default=0)
    num_images_downloaded = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.download_id

class TemporaryRegistration(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=100)  # Example field
    # Add other necessary fields
    created_at = models.DateTimeField(auto_now_add=True)



#####after endsem########## models.py
# from django.db import models

# class Annotation(models.Model):
#     image_name = models.CharField(max_length=255)  # Example field
#     user_text = models.TextField()
#     status = models.CharField(max_length=20, default='Unverified')
#     feedback = models.TextField(null=True, blank=True)  # Optional for verifier's feedback

#     def __str__(self):
#         return self.image_name
