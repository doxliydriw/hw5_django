from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


def check_superusers(id_list):
    users = User.objects.filter(id__in=id_list)
    for user in users:
        if user.is_superuser:
            return True
    return False


class Command(BaseCommand):
    help = "Deletes users as per given ID's"

    def add_arguments(self, parser):
        parser.add_argument("user_id", nargs="+", type=int, help="")

    def handle(self, *args, **options):
        id_list = set(options.get("user_id"))
        users = User.objects.all()
        user_ids = set(user.id for user in users)
        print(user_ids)
        if not user_ids.issuperset(id_list):
            lost_ids = str(id_list.difference(user_ids)).replace("{", '').replace("}", '')
            print(f'Users with IDs {lost_ids} are not found in system')
            id_list.intersection_update(user_ids)
        id_list = list(id_list)
        if check_superusers(id_list):
            print('One of users in list is a superuser and could not be deleted')
        else:
            User.objects.filter(id__in=id_list).delete()
            print('Users with IDs', id_list, 'have been deleted')
            users = User.objects.all()
            user_ids = set(user.id for user in users)
            print('Users left ', user_ids)
