from random import  randint, randrange
from faker import Faker
import logging
from apps.users.models import Users
from django.core.management.base import BaseCommand, CommandError

logging.getLogger('faker').setLevel(logging.ERROR)

class Command(BaseCommand):

    help = "Command informations"

    def handle(self, *args, **kwargs):
        fake = Faker(locale="en_IN")

        print('======================== Stard admins DB Seed process =======================')
        
        try:
            user = Users()
            user.email           = 'sachu@aventusinformatics.com'
            user.username        = 'Admin'
            user.full_name       = "Admin"
            user.mobile           = "8157864536"
            user.set_password("123")
            user.is_verified     = 1
            user.is_admin        = 1
            user.is_active       = 1
            user.is_superuser    = 1
            user.is_staff        = 1
            user.save()
        except Exception as e:
            pass
        
        
        try:

            for i in range(0,10):
                
                first_name = fake.name()
                last_name = fake.name()
                username = "{} {}{}".format(first_name,last_name,randint(10,10000))
                
                if Users.objects.filter(username__contains=username).count() == 0:
                    user = Users()
                    user.email           = fake.email()
                    user.username        = username
                    user.full_name       = "{} {}".format(first_name,last_name)
                    user.mobile           = fake.phone_number()
                    user.set_password("1234")
                    user.is_verified     = 1
                    user.is_admin        = 1
                    user.is_active       = 1
                    user.is_superuser    = 0
                    user.is_staff        = 1
                    user.save()

        except Exception as e:
            pass
        print('======================== End admins DB Seed process =======================')
        
