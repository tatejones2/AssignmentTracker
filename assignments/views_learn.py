"""
Views for the learn/podcast functionality.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.conf import settings
import os
from .models import Podcast, StudyNotes
from .forms import PodcastForm, StudyNotesForm
from .podcast_service import generate_podcast_script, generate_podcast_audio, generate_study_notes
from .file_utils import extract_text_from_file


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
        form = PodcastForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.user = request.user
            
            # Extract text from uploaded file if provided
            if request.FILES.get('notes_file'):
                try:
                    extracted_text = extract_text_from_file(request.FILES['notes_file'])
                    # If there's already notes_text, append the extracted text
                    if podcast.notes_text:
                        podcast.notes_text += "\n\n--- Extracted from uploaded document ---\n" + extracted_text
                    else:
                        podcast.notes_text = extracted_text
                except Exception as e:
                    messages.warning(request, f'Note: Could not extract text from file: {str(e)}')
            
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
            
            # Generate audio with proper media path
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'podcasts', 'audio')
            os.makedirs(audio_dir, exist_ok=True)
            
            audio_filename = f'podcast_{podcast.pk}.mp3'
            audio_full_path = os.path.join(audio_dir, audio_filename)
            
            generate_podcast_audio(script, audio_full_path)
            podcast.audio_file = f'podcasts/audio/{audio_filename}'
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


@login_required
def study_notes_hub(request):
    """Display the study notes hub with all generated notes."""
    study_notes = StudyNotes.objects.filter(user=request.user)
    
    context = {
        'study_notes': study_notes,
    }
    return render(request, 'learn/study_notes_hub.html', context)


@login_required
def study_notes_create(request):
    """Create and generate AI study notes from a topic."""
    if request.method == 'POST':
        form = StudyNotesForm(request.POST, user=request.user)
        if form.is_valid():
            study_note = form.save(commit=False)
            study_note.user = request.user
            study_note.save()
            
            try:
                # Generate study notes
                content = generate_study_notes(
                    topic=study_note.topic,
                    detail_level=study_note.detail_level
                )
                study_note.content = content
                study_note.is_generated = True
                study_note.save()
                
                messages.success(request, 'Study notes generated successfully!')
                return redirect('study_notes_detail', pk=study_note.pk)
            
            except Exception as e:
                messages.error(request, f'Error generating study notes: {str(e)}')
                return redirect('study_notes_detail', pk=study_note.pk)
    else:
        form = StudyNotesForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'learn/study_notes_form.html', context)


@login_required
def study_notes_detail(request, pk):
    """Display study notes details."""
    study_note = get_object_or_404(StudyNotes, pk=pk, user=request.user)
    
    context = {
        'study_note': study_note,
    }
    return render(request, 'learn/study_notes_detail.html', context)


@login_required
def study_notes_delete(request, pk):
    """Delete study notes."""
    study_note = get_object_or_404(StudyNotes, pk=pk, user=request.user)
    
    if request.method == 'POST':
        study_note.delete()
        messages.success(request, 'Study notes deleted successfully!')
        return redirect('study_notes_hub')
    
    context = {
        'study_note': study_note,
    }
    return render(request, 'learn/study_notes_confirm_delete.html', context)
