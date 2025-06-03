from django import template

register = template.Library()

@register.filter
def get_submission_for(submissions, student):
    try:
        return submissions.get(student=student)
    except Submission.DoesNotExist:
        return None
        
@register.filter
def content_type_icon(content_type):
    icon_map = {
        'text': 'file-alt',
        'file': 'file-upload',
        'video': 'video',
        'audio': 'music',
        'assignment': 'tasks',
        'link': 'external-link-alt'
    }
    return icon_map.get(content_type, 'question-circle')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)