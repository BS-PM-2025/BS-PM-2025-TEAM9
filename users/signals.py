# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def create_assignment_for_section_content(sender, instance, created, **kwargs):
    from users.models import SectionContent, Assignment

    if sender.__name__ == 'SectionContent' and created:
        if instance.content_type == 'assignment':
            Assignment.objects.create(
                content=instance,
                # instructions=instance.assignment_instructions,
                deadline=instance.assignment_due_date
            )
