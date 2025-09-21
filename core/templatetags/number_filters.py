from django import template
from core.utils import convert_nepali_to_english_numbers

register = template.Library()

@register.filter
def nepali_to_english(value):
    """
    Convert Nepali numbers to English numbers
    """
    return convert_nepali_to_english_numbers(value)
