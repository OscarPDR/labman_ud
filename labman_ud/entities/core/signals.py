from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.conf import settings

from entities.core.models import BaseModel
from entities.core.tasks import save_rdf, delete_rdf

use_virtuoso = getattr(settings, 'D2R_TO_VIRTUOSO', None)

@receiver(post_save)
def post_save_callback(sender, instance, *args, **kwargs):
    if use_virtuoso and issubclass(sender, BaseModel):
        if not kwargs['created']:
            # It's an update

            # instance and instance.id:
            # past_instance = sender.objects.get(id=instance.id)
            delete_rdf.delay(instance)
        save_rdf.delay(instance)

@receiver(pre_delete)
def post_delete_callback(sender, instance, *args, **kwargs):
    if use_virtuoso and issubclass(sender, BaseModel):
        delete_rdf.delay(instance)

@receiver(m2m_changed)
def m2m_changed_callback(sender, instance, *args, **kwargs):
    if use_virtuoso and issubclass(sender, BaseModel):
        if not kwargs['created']:
            # It's an update
            delete_rdf.delay(instance)
        save_rdf.delay(instance)
