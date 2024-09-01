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

class VideoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()

    def video_info(self, obj):
        return {
            'content_loc': obj.video_file.url,
            'title': obj.title,
            'description': obj.description,
            'thumbnail_loc': obj.thumbnail.url if obj.thumbnail else None,
            'player_loc': self.location(obj),
            'duration': int(obj.duration.total_seconds()) if obj.duration else None,
            'publication_date': obj.created_at.isoformat(),
        }
