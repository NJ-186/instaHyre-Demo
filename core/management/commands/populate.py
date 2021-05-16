
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from random import randint, choice
from datetime import timedelta, datetime

from core.models import User, GlobalDatabase
from core.data import names, phones, mails, passwords


# Populate global database
# No security here as just used for testing purpose

class Command(BaseCommand):
    help = 'Populates the database.'

    def add_arguments(self, parser):
        parser.add_argument('--users',
            default = 15,
            type = int ,
            help = 'The number of users to create.')

        parser.add_argument('--global',
            default = 15,
            type = int ,
            help = 'The number of persons to add in global data.')


    def handle(self, *args, **options):
    
        users_list =  User.objects.none() # to store list of new random users made which will be used while creating random data for global database

        if options['users']:
            i = 0 #counter for phones ( unique )
            for _ in range(options['users']):

                name = choice(names)
                phone = phones[i]
                mail = choice(mails)
                password = choice(passwords)
                i+=1

                user = User.objects.create(
                    name = name,
                    phone = phone,
                    email = mail,
                )

                user.set_password(password)
                user.save()

                users_list |= User.objects.filter(phone = user.phone) # adding freshly made 'user' to users_list

                # Adding the registered user to the global database
                GlobalDatabase.objects.create(
                    name = name,
                    phone = phone,
                    email = mail,
                    registration_status = True,
                    user = user
                )
        
        if options['global']:
            for _ in range(options['global']):
                GlobalDatabase.objects.create(
                    name = choice(names),
                    phone = choice(phones),
                    email = choice(mails),
                    user = users_list[randint(0, users_list.count() - 1)]
                )