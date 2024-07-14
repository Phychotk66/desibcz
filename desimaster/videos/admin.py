from django.contrib import admin
from .models import Video, Category, SubCategory, Tag

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'created_at')
    list_filter = ('category', 'subcategory', 'tags')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Tag)
