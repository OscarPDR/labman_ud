
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify


class FeedWrapper(object):
    def __init__(self, feed_instance):
        self.feed_instance = feed_instance

    def __call__(self, request, *args, **kwargs):
        response = self.feed_instance(request, *args, **kwargs)
        response['Content-Type'] = 'application/xml; charset=utf-8'
        return response


def unique_slugify(instance, name_field="name", slug_field="slug", failure=True):
    # If it has already been created, return
    if getattr(instance, 'id'):
        return

    model = type(instance)

    ending = 2
    name = getattr(instance, name_field).encode('utf-8')
    original = slugified = slugify(name)

    avoid_endless = 100000

    while avoid_endless > 0:
        query = {slug_field: slugified}

        if model.objects.filter(**query).count() == 0:
            setattr(instance, slug_field, slugified)
            return

        slugified = '-'.join(original, ending)
        ending += 1
        avoid_endless -= 1

    if failure:
        raise Exception("Error generating unique slug for %s" % instance)


def nslugify(*values):
    slugified_values = [slugify(unicode(value if value is not None else '').encode('utf8')) for value in values]
    return '-'.join(slugified_values)


def get_last_model_update_log_entry(app_label, model_name_list=None):

    if model_name_list:
        model_ids = ContentType.objects.filter(
                app_label=app_label,
                model__in=[x.lower() for x in model_name_list],
            ).values_list('id', flat=True)

    else:
        model_ids = ContentType.objects.filter(
                app_label=app_label,
            ).values_list('id', flat=True)

    logentries = LogEntry.objects.filter(content_type_id__in=model_ids).order_by('-action_time')

    if len(logentries) > 0:
        return logentries[:1][0]

    else:
        return None
