#Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .utils import calculate_similarity




# User Profile Model
class UserProfile(models.Model):
    """
    The UserProfile model extends the base Django User model to store additional user information.
    Each user will have a one-to-one link with a user profile, which contains details like user type,
    language preferences, and usage statistics.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100)
    languages = models.ManyToManyField('Language', blank=True)
    dark_mode_enabled = models.BooleanField(default=False)
    images_downloaded_count = models.IntegerField(default=0, help_text='Count of images downloaded by the user')
    annotations_downloaded_count = models.IntegerField(default=0, help_text='Count of annotations downloaded by the user')
    images_annotated_count = models.IntegerField(default=0, help_text='Count of images annotated by the user')
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    def clean(self):
        # Ensure annotators have at least one language selected
        if self.user_type == 'Annotator' and not self.languages.exists():
            raise ValidationError({'languages': 'Annotators must select at least one language.'})
    # Accessor for first_name
    @property
    def first_name(self):
        return self.user.first_name

    # Accessor for last_name
    @property
    def last_name(self):
        return self.user.last_name

    # Accessor for email
    @property
    def email(self):
        return self.user.email
# Language Model
class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return self.name

# Image Model
class Image(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_confidential = models.BooleanField(default=False, verbose_name="Confidential Image")
    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ('title', 'language')
    
# Annotation Model
class Annotation(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    annotation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False, help_text='Indicates if the annotation has been validated')
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_annotations', help_text='User who validated the annotation')
    # similarity_score = models.FloatField(default=1.0, help_text='Average similarity score with other annotations')

    def __str__(self):
        return f"Annotation for {self.image.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update user profile count after saving an annotation
        self.annotator.userprofile.images_annotated_count += 1
        self.annotator.userprofile.save()
        # In models.py, within the Annotation class

        # Trigger similarity calculation and validation here.
        # self.calculate_and_update_similarity()

    # def calculate_and_update_similarity(self):
    #     annotations = Annotation.objects.filter(image=self.image).exclude(id=self.id)
        
    #     if annotations.exists():
    #         # Step 1: Count occurrences of each unique annotation
    #         annotation_counts = {}
    #         for annotation in annotations:
    #             if annotation.annotation in annotation_counts:
    #                 annotation_counts[annotation.annotation] += 1
    #             else:
    #                 annotation_counts[annotation.annotation] = 1
            
    #         # Step 2: Determine the most common annotation(s)
    #         max_count = max(annotation_counts.values())
    #         most_common_annotations = [annotation for annotation, count in annotation_counts.items() if count == max_count]
            
    #         # Step 3: Determine validity based on majority voting
    #         self.validated = self.annotation in most_common_annotations

    #         # Update the similarity score (optional, set to 1.0 for majority-voted annotations)
    #         self.similarity_score = 1.0 if self.validated else 0.0

    #     else:
    #         # If there are no other annotations for the image, consider this one as valid by default
    #         self.validated = True
    #         self.similarity_score = 1.0  # Set a high similarity score for a single annotation
        
    #     # Save the updated fields
    #     self.save(update_fields=['similarity_score', 'validated'])



# Remark Model
class Remark(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    researcher = models.ForeignKey(User, related_name='researcher_remarks', on_delete=models.CASCADE)
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark on {self.annotation.image.title}"

# Download Model
class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    annotation = models.ForeignKey(Annotation, on_delete=models.SET_NULL, null=True, blank=True)
    download_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Download by {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update user profile counts after saving a download
        user_profile = self.user.userprofile
        if self.image:
            user_profile.images_downloaded_count += 1
        if self.annotation:
            user_profile.annotations_downloaded_count += 1
        user_profile.save()


# Assignment Model
class Assignment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    annotator = models.ForeignKey(User, related_name='assigned_images', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, related_name='assignments_made', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, null=True)  # e.g., 'Assigned', 'Completed'
    # Other fields as needed

    def __str__(self):
        return f"Assignment for {self.image.title} to {self.annotator.username}"

#selected annotators
from django.db import models
from django.contrib.auth.models import User

class SelectedAnnotators(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selected_by')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='selected_language')
    annotators = models.ManyToManyField(User, related_name='annotators')

    def __str__(self):
        return f"Selected Annotators for {self.language.name} by {self.user.username}"

    def get_tabular_representation(self):
        annotators_str = ', '.join([str(annotator) for annotator in self.annotators.all()])
        return [str(self.user), self.language.name, annotators_str]
    
    
    
    
class ValidationTask(models.Model):
    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Validated', 'Validated'),
    ]

    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    validator = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, related_name='validation_tasks_created', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Assigned')

    def __str__(self):
        return f"Validation Task for {self.annotation} assigned to {self.validator.username}"
    
    class Meta:
        unique_together = ['annotation', 'validator', 'status', 'assigned_by']
        
        
        

from django.db import models
from django.contrib.auth.models import User

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback")
    ui_rating = models.IntegerField()
    ui_feedback = models.TextField()
    image_upload_rating = models.IntegerField(null=True, blank=True)  # Optional based on user role
    image_upload_feedback = models.TextField(null=True, blank=True)
    annotation_process_rating = models.IntegerField()
    annotation_process_feedback = models.TextField()
    validation_process_rating = models.IntegerField(null=True, blank=True)
    validation_process_feedback = models.TextField(null=True, blank=True)
    overall_software_rating = models.IntegerField()
    overall_feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"




# In your Django app's models.py file

from django.db import models

class OTPModel(models.Model):
    email = models.EmailField(max_length=254)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email}"
