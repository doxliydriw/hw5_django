from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker


class Command(BaseCommand):
    help = 'Creates new users according to given argument of quantity'

    def add_arguments(self, parser):
        parser.add_argument("user_qty", type=int, help="This is a quantity of users to be created")

    def handle(self, *args, **options):
        qty = int(options.get("user_qty"))
        if 0 < qty < 10:
            i = 0
            fake = Faker()
            while i < qty:
                user = User.objects.create_user(fake.first_name().lower(), email=fake.email(), password=fake.password())
                user.save()
                i += 1
        else:
            print('User quantity must be more then 0 but less then 10')
        print(User.objects.all())
