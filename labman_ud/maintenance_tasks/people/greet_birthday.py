# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.mail import send_mail
from entities.persons.models import Person

from datetime import date


###########################################################################
# def: greet_birthday()
###########################################################################

def greet_birthday():
    print '#' * 80
    print 'Checking for members birthdays...'
    print '#' * 80

    members = Person.objects.filter(is_active=True)

    for member in members:
        birth_date = member.birth_date

        if birth_date:
            today = date.today()

            if (birth_date.day == today.day) and (birth_date.month == today.month):
                print '\tToday is %s\'s birthday!' % member.full_name

                try:
                    send_mail(
                        'Happy B-day %s... ;^)' % member.full_name,     # Subject
                        '¡Felicidades!\nZorionak!\nHappy birthday!',      # Message
                        getattr(settings, 'EMAIL_SENDER_ADDRESS', ''),  # From
                        getattr(settings, 'GENERAL_NOTIFICATIONS_ADDRESSES', []),   # To
                        fail_silently=False
                    )
                except:
                    print '\t\tUnable to send e-mail'
