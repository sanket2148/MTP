# newapp/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Language


# from .utils import calculate_similarity
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Annotation, UserProfile




@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(Language)
    permission, created = Permission.objects.get_or_create(
        codename='view_all_languages',
        name='Can view all languages',
        content_type=content_type,
    )


# @receiver(post_save, sender=Annotation)
# def update_annotation_similarity_scores_and_validation(sender, instance, created, **kwargs):
#     if created:  # Ensures this runs only for newly created annotations
#         # Update similarity scores and validation for all annotations of the image
#         annotations = Annotation.objects.filter(image=instance.image).exclude(id=instance.id)
#         for other_annotation in annotations:
#             # Assume calculate_similarity_score is a new function that calculates and updates the instance
#             calculate_similarity_score(instance, other_annotation)
#         instance.annotator.userprofile.images_annotated_count += 1

#         instance.annotator.userprofile.save()

# def calculate_similarity_score(new_annotation, other_annotation):
#     # Implement the logic to calculate and update similarity scores
#     # This is a placeholder for the actual similarity calculation logic
#     similarity_score = calculate_similarity(new_annotation.annotation, other_annotation.annotation)
#     other_annotation.similarity_score = similarity_score
#     other_annotation.validated = similarity_score > 0.8  # Example threshold
#     other_annotation.save(update_fields=['similarity_score', 'validated'])
