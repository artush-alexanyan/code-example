from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from auth2.exceptions import CantBuySecretToys, ToyLimitReached, ToyAlreadyCollected
from auth2.models import User
from gift.models import Gift, Event
from toy.models import ToyPage, is_already_collected


class Command(BaseCommand):
    help = 'Gift the toy.'

    def add_arguments(self, parser):
        parser.add_argument('--event', type=str)

    def give(self, toys, user: User):
        for toy in toys:
            self.stdout.write(self.style.WARNING(f'Prepare gift of the toy `{toy}` to `{user}`'))
            try:
                user.gift(toy)
            except CantBuySecretToys:
                self.stdout.write(self.style.WARNING(f'Can not add secret toy: {toy}'))
                continue
            except ToyLimitReached:
                self.stdout.write(self.style.WARNING(f'Toy `{toy}` limit reached'))
                continue
            except ToyAlreadyCollected:
                self.stdout.write(self.style.WARNING(f'User already collected `{toy}`'))
                continue
            else:
                if is_already_collected(toy, user):
                    self.stdout.write(self.style.SUCCESS(f'COLLECTED OK!'))
                else:
                    self.stdout.write(self.style.WARNING(f'NOT GIFTED!'))

    def handle(self, *args, **options):
        try:
            event = Event.objects.get(name__iexact=options['event'])
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'No event with name {options["event"]}'))
            exit(1)

        toys = ToyPage.objects.live().filter(is_secret=False).filter(date__lte=event.start_datetime)
        event_gifts = Gift.objects.filter(event=event)
        cnt = 0
        for gift in event_gifts:
            if gift.is_used() and not gift.gifted:
                self.give(toys, gift.user)
                gift.gifted = True
                cnt += 1
                gift.save()
        self.stdout.write(f"Gifted users: {cnt}")
        # if options['email']:
        #     try:
        #         user = User.objects.get(email=options['email'])
        #     except ObjectDoesNotExist:
        #         self.stdout.write(self.style.ERROR('No user with email: %s' % options['email']))
        #         exit(1)
        #     else:
        #         self.give(toys, user)
        # elif options['who_owns_toy_id']:
        #     users = User.objects.filter(toys__id=options['who_owns_toy_id'])
        #     for cnt, user in enumerate(users, 1):
        #         self.give(toys, user)
        #     self.stdout.write(self.style.SUCCESS(f'Users processed: {cnt}'))



