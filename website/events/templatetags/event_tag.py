from django import template
from events.models import Category, Event

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('events/tags/last_event.html')
def get_last_events(count=5):
    events = Event.objects.order_by('id')[:count]
    return {'last_events': events}