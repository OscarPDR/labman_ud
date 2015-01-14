
class FeedWrapper(object):
    def __init__(self, feed_instance):
        self.feed_instance = feed_instance

    def __call__(self, request, *args, **kwargs):
        response = self.feed_instance(request, *args, **kwargs)
        response['Content-Type'] = 'application/xml; charset=utf-8'
        return response
