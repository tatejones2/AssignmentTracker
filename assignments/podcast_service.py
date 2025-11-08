"""
Service for generating AI podcasts using OpenAI.
"""
import os
from openai import OpenAI

# Initialize client with API key from environment
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) if api_key else None


def generate_podcast_script(topic, notes_text, tone='educational', length='medium', description=''):
    """
    Generate a podcast script from notes using OpenAI's GPT.
    
    Args:
        topic: Main topic of the podcast
        notes_text: The notes or content to convert
        tone: Tone of the podcast ('casual', 'professional', 'educational', 'motivational')
        length: Target length ('short', 'medium', 'long')
        description: Additional context
    
    Returns:
        str: Generated podcast script
    """
    
    if not client:
        raise Exception("OpenAI API key not configured. Please set OPENAI_API_KEY in .env file.")
    
    # Define length guidelines
    length_map = {
        'short': '5-10 minutes',
        'medium': '10-20 minutes',
        'long': '20-30 minutes'
    }
    
    length_guidance = length_map.get(length, '10-20 minutes')
    
    # Create the prompt
    prompt = f"""You are an expert podcast script writer. Create an engaging and informative podcast script based on the following information.

Topic: {topic}
Tone: {tone}
Target Duration: {length_guidance}
{f'Additional Context: {description}' if description else ''}

Notes/Content to Convert:
{notes_text}

Please create a podcast script that:
1. Has a catchy introduction that hooks the listener
2. Breaks down the information into logical segments
3. Uses natural, conversational language
4. Includes transitions between sections
5. Ends with a memorable conclusion
6. Includes [MUSIC] and [PAUSE] markers where appropriate
7. Is appropriate for the specified tone and target duration

Format the script as:
[INTRO MUSIC]
[Host introduction and hook]
[Content sections with clear breaks]
[Conclusion]
[OUTRO MUSIC]

Generate the podcast script now:"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional podcast script writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating podcast script: {str(e)}")


def generate_podcast_audio(script, filename):
    """
    Generate audio from a podcast script using OpenAI's Text-to-Speech.
    
    Args:
        script: The podcast script text
        filename: Output filename for the audio file
    
    Returns:
        str: Path to the generated audio file
    """
    
    try:
        # Use OpenAI's text-to-speech API
        speech_file_path = filename
        
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice="nova",
            input=script
        )
        
        response.stream_to_file(speech_file_path)
        return speech_file_path
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")
