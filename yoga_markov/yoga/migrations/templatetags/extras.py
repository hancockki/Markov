from django import template
from random import randint
import collage

register = template.Library()


@register.simple_tag
def collage_test():
    return randint(0,999)