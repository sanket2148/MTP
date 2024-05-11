from django.contrib import admin
from .models import UserProfile, Image, Annotation, Download, Language , SelectedAnnotators

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','first_name', 'last_name', 'user_type', 'get_languages')
    list_filter = ('user', 'user_type',"languages")
    search_fields = ('user__username', 'user_type','user__first_name')

    def get_languages(self, obj):
        return ", ".join([language.name for language in obj.languages.all()])
    get_languages.short_description = 'Languages'
    
    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', "image",'language', 'uploaded_by', 'created_at', 'is_confidential']  # Update list_display
    list_filter = ('language', 'uploaded_by', 'is_confidential')  # Update field names
    search_fields = ('title', 'uploaded_by__username','language')
    def image_size(self, obj):
        if obj.image:
            return f"{obj.image.size / 1024:.2f} KB"  # Size in kilobytes
        return "Unknown"
    image_size.short_description = 'Image Size'
    
    
# Custom admin for Annotation
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('id','language','image', 'annotator', 'annotation', 'created_at','validated',"validated_by")  # Update field names
    list_filter = ('language', 'created_at','annotator','image','validated_by')  # Update field names
    search_fields = ('image__title', 'annotator__username', 'annotation')

# Custom admin for Download
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user', 'download_type', 'created_at')  # Update field names
    list_filter = ('download_type', 'created_at')  # Update field names
    search_fields = ('user__username',)


from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id','assigned_by', 'annotator','image', 'language')
    list_filter = ('assigned_by', 'annotator','image', 'language') 
    search_fields = ('assigned_by', 'annotator','image', 'language')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id','name']



    
from django.contrib import admin
from .models import SelectedAnnotators

@admin.register(SelectedAnnotators)
class SelectedAnnotatorsAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_languages', 'get_annotators']
    list_filter = ['language', 'annotators']  # Use the correct field names here
    search_fields =('user__usernam','language','annotator')
    
    def get_languages(self, obj):
        return obj.language.name if obj.language else ""
    get_languages.short_description = 'Languages'

    def get_annotators(self, obj):
        return ", ".join([annotator.username for annotator in obj.annotators.all()])
    get_annotators.short_description = 'Annotators'




from .models import ValidationTask

# Register the ValidationTask model
@admin.register(ValidationTask)
class ValidationTaskAdmin(admin.ModelAdmin):
    list_display = ('id','annotation', 'validator', 'assigned_by',  'status')  # Customize the list display
    list_filter = ('status',)
    search_fields = ('annotation__id', 'validator__username', 'assigned_by__username')
    
    
from django.contrib import admin
from .models import UserFeedback  # Adjust the import path according to your app's structure

# Optional: Define a custom admin view to improve interface usability
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'ui_rating',"ui_feedback","image_upload_rating","image_upload_feedback", 'annotation_process_rating',"annotation_process_feedback","validation_process_rating","validation_process_feedback", 'overall_software_rating',"overall_feedback", 'created_at')  # Customize to display relevant fields
    list_filter = ('created_at', 'ui_rating', 'overall_software_rating')  # Filter options
    search_fields = ('user__username', 'ui_feedback', 'annotation_process_feedback', 'overall_feedback')  # Search functionality
    readonly_fields = ('created_at',)  # Fields that should not be editable

# Register your models here.
    
admin.site.register(UserFeedback, UserFeedbackAdmin)   
# Register your models here
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Language, LanguageAdmin)
#admin.site.register(ValidationTask, ValidationTaskAdmin)
# admin.site.register(SelectedAnnotators,SelectedAnnotatorsAdmin)
