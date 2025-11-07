"""
Context processors for passing data to all templates.
"""
import random
from .quotes_tips import MOTIVATIONAL_QUOTES, STUDY_TIPS


def quotes_and_tips(request):
    """Add a random quote and tip to the context for all views."""
    if request.user.is_authenticated:
        # Get a random quote and tip
        quote = random.choice(MOTIVATIONAL_QUOTES)
        tip = random.choice(STUDY_TIPS)
        
        return {
            'sidebar_quote': quote,
            'sidebar_tip': tip,
        }
    return {}
