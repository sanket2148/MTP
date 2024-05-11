from django.contrib import admin
from .models import UserProfile, Image, Annotator, Annotation, Download, LanguageFolder

# Custom admin for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'get_languages')
    search_fields = ('user__username', 'user_type')

    def get_languages(self, obj):
        return ", ".join([language.name for language in obj.languages.all()])
    get_languages.short_description = 'Languages'

# Custom admin for Image
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_name', 'get_language_folder']

    def get_language_folder(self, obj):
        return obj.language_folder
    get_language_folder.short_description = 'Language Folder'

# Custom admin for Annotator
class AnnotatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_languages')
    filter_horizontal = ('languages',)  # For easier management of ManyToMany field
    search_fields = ('user__username',)

    def get_languages(self, obj):
        return ", ".join([language.name for language in obj.languages.all()])
    get_languages.short_description = 'Languages'

# Custom admin for Annotation
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('annotation_id', 'image', 'annotator', 'language', 'timestamp')
    search_fields = ('annotation_id', 'image__image_name', 'annotator__user__username')
    list_filter = ('language', 'timestamp')

# Custom admin for Download
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('download_id', 'user', 'download_type', 'num_annotations_downloaded', 'num_images_downloaded', 'timestamp')
    search_fields = ('download_id', 'user__username')
    list_filter = ('download_type', 'timestamp')

# Custom admin for Language
class LanguageFolderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# class AnnotationAdmin(admin.ModelAdmin):
#     list_display = ('annotation_id', 'image', 'annotator', 'language', 'timestamp', 'status', 'feedback')
#     search_fields = ('annotation_id', 'image__image_name', 'annotator__user__username', 'language')
#     list_filter = ('language', 'timestamp', 'status')
#     actions = ['approve_annotations', 'reject_annotations']

#     def approve_annotations(self, request, queryset):
#         queryset.update(status='Verified')
#     approve_annotations.short_description = "Mark selected annotations as verified"

#     def reject_annotations(self, request, queryset):
#         queryset.update(status='Rejected')
#     reject_annotations.short_description = "Mark selected annotations as rejected"



# Registering models with custom admins
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Annotator, AnnotatorAdmin)
admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(LanguageFolder, LanguageFolderAdmin)
