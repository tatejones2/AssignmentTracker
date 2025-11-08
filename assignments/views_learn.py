"""
Views for the learn/podcast functionality.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
import os
from .models import Podcast
from .forms import PodcastForm
from .podcast_service import generate_podcast_script, generate_podcast_audio


@login_required
def learn_hub(request):
    """Display the learn hub with all podcasts."""
    podcasts = Podcast.objects.filter(user=request.user)
    
    context = {
        'podcasts': podcasts,
    }
    return render(request, 'learn/learn_hub.html', context)


@login_required
def podcast_create(request):
    """Create a new podcast from notes."""
    if request.method == 'POST':
        form = PodcastForm(request.POST, user=request.user)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.user = request.user
            podcast.save()
            
            messages.success(request, 'Podcast created! Now generating script...')
            return redirect('podcast_generate', pk=podcast.pk)
    else:
        form = PodcastForm(user=request.user)
    
    context = {
        'form': form,
        'action': 'Create'
    }
    return render(request, 'learn/podcast_form.html', context)


@login_required
def podcast_generate(request, pk):
    """Generate podcast script and audio."""
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            # Generate script
            script = generate_podcast_script(
                topic=podcast.topic,
                notes_text=podcast.notes_text,
                tone=podcast.tone,
                length=podcast.length,
                description=podcast.description
            )
            podcast.script = script
            podcast.is_generated = True
            
            # Generate audio
            audio_filename = f'podcasts/audio/podcast_{podcast.pk}.mp3'
            os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
            
            audio_path = generate_podcast_audio(script, audio_filename)
            podcast.audio_file = audio_filename
            podcast.is_audio_generated = True
            
            podcast.save()
            messages.success(request, 'Podcast generated successfully!')
            return redirect('podcast_detail', pk=podcast.pk)
            
        except Exception as e:
            messages.error(request, f'Error generating podcast: {str(e)}')
            return redirect('podcast_detail', pk=podcast.pk)
    
    context = {
        'podcast': podcast,
    }
    return render(request, 'learn/podcast_generate.html', context)


@login_required
def podcast_detail(request, pk):
    """Display podcast details and script."""
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    
    context = {
        'podcast': podcast,
    }
    return render(request, 'learn/podcast_detail.html', context)


@login_required
def podcast_download(request, pk):
    """Download podcast audio file."""
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    
    if podcast.audio_file:
        file_path = podcast.audio_file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'{podcast.title}.mp3')
    
    messages.error(request, 'Audio file not found.')
    return redirect('podcast_detail', pk=podcast.pk)


@login_required
def podcast_delete(request, pk):
    """Delete a podcast."""
    podcast = get_object_or_404(Podcast, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Delete audio file if exists
        if podcast.audio_file:
            if os.path.exists(podcast.audio_file.path):
                os.remove(podcast.audio_file.path)
        
        podcast.delete()
        messages.success(request, 'Podcast deleted successfully!')
        return redirect('learn_hub')
    
    context = {
        'podcast': podcast,
    }
    return render(request, 'learn/podcast_confirm_delete.html', context)
