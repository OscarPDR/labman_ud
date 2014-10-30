
from django.conf import settings
from django.core.urlresolvers import reverse

from labman_setup.models import *

import requests
import tweetpony


def post_tweet(news_instance):

    tweetpony_config = _get_tweetpony_configuration()
    base_url = _get_base_url()

    if tweetpony_config and base_url:
        news_url = '%s%s' % (base_url, reverse('view_news', kwargs={'news_slug': news_instance.slug}))

        tweetpony_api = tweetpony.API(
            consumer_key=tweetpony_config.consumer_key,
            consumer_secret=tweetpony_config.consumer_secret,
            access_token=tweetpony_config.access_token,
            access_token_secret=tweetpony_config.access_token_secret,
        )

        print news_url

        if (tweetpony_config.karmacracy_username and tweetpony_config.karmacracy_api_key):
            tweet_url = _get_short_url(news_url, tweetpony_config)

        else:
            tweet_url = news_url

        tweet_text = _generate_tweet_text(news_instance)

        tweet = '%s: %s' % (tweet_text, tweet_url)

        try:
            tweetpony_api.update_status(status=tweet)

        except tweetpony.APIError as err:
            print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)


def _get_tweetpony_configuration():
    try:
        return TweetPonyConfiguration.objects.get()

    except:
        print 'TweetPonyConfiguration object not filled'
        return None


def _get_base_url():
    if settings.DEBUG:
        return 'localhost:8000'

    else:
        return getattr(settings, 'BASE_URL', '')


def _get_short_url(full_news_url, tweetpony_config):
    karmacracy_username = tweetpony_config.karmacracy_username
    karmacracy_api_key = tweetpony_config.karmacracy_api_key

    karmacracy_base_url = "http://kcy.me/api/?u=%s&key=%s&url=" % (karmacracy_username, karmacracy_api_key)

    full_url = '%s%s' % (karmacracy_base_url, full_news_url)

    if (tweetpony_config.http_proxy and tweetpony_config.https_proxy):
        proxies = {
            'http': tweetpony_config.http_proxy,
            'https': tweetpony_config.https_proxy,
        }

        request = requests.get(full_url, proxies=proxies)

    else:
        request = requests.get(full_url)

    return request.text


def _generate_tweet_text(news_instance):
    if news_instance.cc:
        cc_text = "cc %s" % news_instance.cc

    else:
        cc_text = ''

    cc_length = len(cc_text)

    title_length = len(news_instance.title)

    if (cc_length == 0):

        if (title_length < 120):
            tweet_text = news_instance.title

        else:
            new_title_length = 120 - 3
            tweet_text = "%s..." % news_instance.title[:new_title_length]

    else:
        if ((title_length + cc_length) < 120):
            tweet_text = "%s %s" % (news_instance.title, cc_text)

        else:
            new_title_length = 120 - cc_length - 4
            tweet_text = "%s... %s" % (news_instance.title[:new_title_length], cc_text)

    return tweet_text
