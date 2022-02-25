from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from auth2.models import User
from gift.models import Gift, Event
from toy.models import ToyPage, ToyCollection


class Command(BaseCommand):
    help = "Move owners of Gamma's toy to gamma event."

    def add_arguments(self, parser):
        parser.add_argument('--pk', type=int, dest='pk')
        parser.add_argument('--event', type=str)

    def handle(self, *args, **options):
        toy = ToyPage.objects.get(pk=options['pk'])
        event = Event.objects.get(name=options['event'])
        owners = User.objects.filter(toys=toy)
        for cnt, user in enumerate(owners):
            obj = ToyCollection.objects.get(toy=toy, user=user)
            print(user, ' ', obj.created, ' ', user.toys.count())
            try:
                gift = Gift.objects.get(event=event, user=user, toy=toy)
            except ObjectDoesNotExist:
                print('CREATED')
                gift_obj, is_created = Gift.objects.get_or_create(toy=toy, user=user,
                                                                  redeemed=1,
                                                                  max_usages=1,
                                                                  event=event,
                                                                  created=obj.created,
                                                                  modified=obj.created
                                                                  )
        print(f'{toy}: {cnt}')
