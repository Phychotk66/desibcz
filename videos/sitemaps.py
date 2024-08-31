from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Video, Category, SubCategory

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['videos:home', 'videos:video_list_all', 'videos:upload_video']

    def location(self, item):
        return reverse(item)

class VideoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('videos:video_list', args=[obj.id])

class SubCategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return SubCategory.objects.all()

    def location(self, obj):
        return reverse('videos:video_list', args=[obj.category.id, obj.id])
