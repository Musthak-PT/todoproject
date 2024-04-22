from random import  randint, random, randrange
from faker import Faker
import logging
from apps.users.models import Users
from django.core.management.base import BaseCommand, CommandError

logging.getLogger('faker').setLevel(logging.ERROR)

class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker(locale="en_IN")

        print('======================== Stard users DB Seed process =======================')

        for i in range(0,100):
            first_name = fake.name()
            last_name = fake.name()
            username = "{} {}".format(first_name,last_name)
            
            if Users.objects.filter(username__contains=username).count() == 0:
                user = Users()
                user.email           = fake.email()
                user.username        = username
                user.first_name      = first_name
                user.last_name       = last_name
                user.phone           = fake.phone_number()
                user.is_verified     = 1
                user.is_admin        = 0
                user.is_active       = 1
                user.is_superuser    = 0
                user.is_staff        = 1
                user.save()


        print('======================== End users DB Seed process =======================')