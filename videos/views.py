from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .models import Video, Category, SubCategory, Tag
from .utils import transcode_video
import os

def upload_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category_id = request.POST['category']
        subcategory_id = request.POST.get('subcategory')
        tags_ids = request.POST.getlist('tags')  # Assuming multiple tags can be selected
        video_file = request.FILES['video_file']
        thumbnail = request.FILES.get('thumbnail')
        duration = request.POST.get('duration')  # Assuming duration is provided

        category = Category.objects.get(id=category_id)
        subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
        tags = Tag.objects.filter(id__in=tags_ids)
        
        video = Video.objects.create(
            title=title,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail,
            category=category,
            subcategory=subcategory,
            duration=duration
        )
        video.tags.set(tags)

        video_dir = os.path.join('media', 'videos', str(video.id))
        os.makedirs(video_dir, exist_ok=True)

        input_video_path = os.path.join('media', video.video_file.name)
        transcode_video(input_video_path, video_dir)

        return redirect('videos:home')

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'tags': tags,
    }
    return render(request, 'upload_video.html', context)

def home(request):
    categories = Category.objects.all()
    latest_videos = Video.objects.order_by('-created_at')
    search_query = request.GET.get('q')

    if search_query:
        latest_videos = latest_videos.filter(title__icontains=search_query)

    paginator = Paginator(latest_videos, 21)  # Show 6 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'latest_videos': page_obj,
        'search_query': search_query,
    }
    return render(request, 'home.html', context)

def video_list(request, category_id=None):
    videos = Video.objects.order_by('-created_at')
    category = None
    search_query = request.GET.get('q')

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        videos = videos.filter(category=category)

    if search_query:
        videos = videos.filter(title__icontains=search_query)

    paginator = Paginator(videos, 21)  # Show 2 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'videos': page_obj,
        'category': category,
        'search_query': search_query,
    }

    return render(request, 'video_list.html', context)


def video_player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_dir = os.path.join('media', 'videos', str(video.id))
    resolutions = []

    # Check if the video directory exists
    if os.path.exists(video_dir):
        # Get the paths of the video files
        for filename in os.listdir(video_dir):
            if filename.endswith('.mp4'):
                video_url = os.path.join('media', 'videos', str(video.id), filename)
                resolutions.append({'width': None, 'height': None, 'video_url': video_url})
    else:
        # Handle the case when the video directory does not exist
        print(f"Error: Video directory not found for video ID {video.id}")
        # You can add additional error handling or fallback logic here

    # If no video files are available, use the original video file
    if not resolutions:
        resolutions.append({'width': None, 'height': None, 'video_url': video.video_file.url})

    # Fetch related videos
    related_videos = video.related_videos.all()

    # Pagination
    paginator = Paginator(related_videos, 9)  # 10 items per page
    page = request.GET.get('page')
    try:
        related_videos_paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        related_videos_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        related_videos_paginated = paginator.page(paginator.num_pages)

    context = {
        'video': video,
        'resolutions': resolutions,
        'related_videos': related_videos_paginated,  # Pass paginated related videos to the context
    }

    return render(request, 'videos/video_player.html', context)
