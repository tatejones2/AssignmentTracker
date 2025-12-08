"""
Views for the chatbot/AI assistant feature.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from openai import OpenAI
import os
from .models import ChatMessage, Course, Assignment
from .forms import ChatForm


def generate_ai_response(question, user_context=""):
    """Generate AI chatbot response using OpenAI."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return "Error: OpenAI API key not configured."
    
    client = OpenAI(api_key=api_key)
    
    system_prompt = f"""You are a helpful academic assistant for a student assignment tracker app called Trax. 
Your role is to help students with:
- Assignment advice and strategies
- Course-related questions
- Study tips and techniques
- Time management for academics
- Motivation and encouragement
- General academic questions

Be friendly, supportive, and concise. Keep responses to 2-3 paragraphs max.
{user_context}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


@login_required
def chatbot_hub(request):
    """Display AI chatbot hub."""
    chat_history = ChatMessage.objects.filter(user=request.user)[:10]
    
    context = {
        'chat_history': chat_history,
    }
    return render(request, 'learn/chatbot_hub.html', context)


@login_required
def chatbot_ask(request):
    """Handle chatbot question."""
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            
            # Get user's course context for better responses
            user_courses = Course.objects.filter(user=request.user)
            course_context = ", ".join([c.course_name for c in user_courses[:5]])
            context_str = f"User is taking courses: {course_context}" if course_context else ""
            
            # Generate response
            response_text = generate_ai_response(question, context_str)
            
            # Save to history
            chat = ChatMessage.objects.create(
                user=request.user,
                question=question,
                response=response_text
            )
            
            messages.success(request, 'Response generated!')
            return redirect('chatbot_hub')
    else:
        form = ChatForm()
    
    context = {
        'form': form,
        'chat_history': ChatMessage.objects.filter(user=request.user)[:10],
    }
    return render(request, 'learn/chatbot_ask.html', context)


@login_required
def chatbot_delete_message(request, pk):
    """Delete a chat message."""
    chat = get_object_or_404(ChatMessage, pk=pk, user=request.user)
    
    if request.method == 'POST':
        chat.delete()
        messages.success(request, 'Message deleted!')
        return redirect('chatbot_hub')
    
    return render(request, 'learn/chatbot_confirm_delete.html', {'chat': chat})


@login_required
def chatbot_clear_all(request):
    """Clear all chat history."""
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
        messages.success(request, 'Chat history cleared!')
        return redirect('chatbot_hub')
    
    return render(request, 'learn/chatbot_confirm_clear.html')
