from django.template.defaulttags import register
from survey.models import Record

def display_violation(value):
    try:
        return dict(Record.VIOLATIONS_CHOICES)[value]
    except KeyError:
        return settings.TEMPLATE_STRING_IF_INVALID
register.filter('display_violation', display_violation)
